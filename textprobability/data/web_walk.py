"""Traverse the Internet via hyperlinks."""

from typing import Callable, Iterable, Iterator, List, Optional, Set
from bs4 import BeautifulSoup
import requests
from numpy.random import Generator

UrlResolver = Callable[[str], str]

NON_TEXTUAL_HTML_TAGS = (
    "style",
    "script",
    "img",
    "meta",
    "nav",
    "figure",
    "figcaption",
    "figure",
    "code",
    "data",
    "var",
    "audio",
    "video",
    "map",
    "video",
    "iframe",
    "embed",
    "object",
    "param",
    "picture",
    "portal",
    "math",
    "svg",
    "canvas",
    "table",
    "base",
    "head",
    "link",
    "kbd",
    "area",
    "track",
    "source",
    "slot",
    "template",
    "form",
    "details",
    "dialog",
    "menu",
    "summary",
)


def web_walk(
    start: str,
    rng: Generator,
    websites: Optional[Set[str]] = None,
    fringe_size: int = 10,
    url_resolver: UrlResolver = lambda s: s,
    exclude=NON_TEXTUAL_HTML_TAGS,
    verbose: bool = False,
) -> Iterator[str]:
    """Iterates over the web pages that are reachable from `start`.
    :param start: The URL of a website
    :param desired_text_len: The desired amount of text (in characters)
    :param rng: The random number generator that determines which sites
        are visited
    :param websites: The set of acceptable websites to explore (e.g.,
        {https://ar.wikipedia.org})
    :param fringe_size: The desired number of websites to explore
        simultaneously
    :param url_resolver: A function for interpreting hyperlinks that
        might otherwise be invalid
    :param exclude: HTML subtree types to exclude from the output, as
        denoted by their HTML tags
    :param verbose: Whether to print verbose output
    """
    visited = set()

    def filtered(soup: BeautifulSoup) -> Iterable[str]:
        return {
            resolved
            for resolved in [
                url_resolver(a.get("href"))
                for a in soup.find_all("a")
                if a.get("href") is not None
            ]
            if resolved not in visited
            and (
                websites is None
                or any(resolved.startswith(website + "/") for website in websites)
            )
        }

    fringe: List[str] = [start]
    while True:
        new_fringe: List[str] = []
        for url in fringe:
            if verbose:
                print("Visiting {}...".format(url))
            visited.add(url)
            try:
                response = requests.get(url_resolver(url))
            except requests.exceptions.RequestException:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.find_all(list(exclude)):
                tag.extract()
            yield soup.get_text()
            new_fringe.extend(filtered(soup))
        if len(new_fringe) > fringe_size:
            new_fringe = list(rng.choice(new_fringe, fringe_size))
        fringe = new_fringe


def get_prefixer(prefix: str, resolver: UrlResolver = lambda x: x) -> UrlResolver:
    """Returns a `UrlResolver` that prefixes otherwise invalid URLs with
    `prefix`.
    """

    def prefixer(url: str) -> str:
        url = resolver(url)
        if url.startswith("http"):
            return url
        return prefix + url

    return prefixer


def get_query_string_remover(resolver: UrlResolver = lambda x: x) -> UrlResolver:
    """Returns a `UrlResolver` that removes the query strings from
    URLs.
    """
    return lambda x: resolver(x).split("?")[0]


def wikipedia_about_page(langcode: str) -> str:
    """Returns the Wikipedia "About" page for the language given by
    `langcode`.
    :param langcode: The language code of the desired language
    """
    return "https://{}.wikipedia.org/wiki/Wikipedia:About".format(langcode)


def wikipedia(langcode: str) -> str:
    """Returns the Wikipedia website for the language given by
    `langcode`.
    :param langcode: The language code of the desired language
    """
    return "https://{}.wikipedia.org".format(langcode)
