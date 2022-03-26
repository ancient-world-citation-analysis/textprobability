"""A language classifier with priors."""

from typing import Callable, Dict

from textprobability.core.defaults import markov, DEFAULT_DATA_PATH
from textprobability.core.types import P


Classifier = Callable[[str], Dict[str, float]]


def _normalize(dist: Dict[str, float]) -> Dict[str, float]:
    total = sum(dist.values())
    if total == 0:  # Not normalizable :(
        return {key: 1 / len(dist) for key in dist}
    return {key: dist[key] / total for key in dist}


def _forceNumber(p: P) -> Callable[[str], float]:
    def ret(s):
        ret = p(s)
        return ret if ret is not None else 0

    return ret


def classifier(priors: Dict[str, float], path=DEFAULT_DATA_PATH) -> Classifier:
    """Return a Classifier with priors proportional to the given priors (which
    need not be normalized).
    :param priors: A map from BCP-47 language codes to numbers that are
    proportional to their prior probabilities.
    """
    markovs = {key: _forceNumber(markov(key, path=path)) for key in priors}
    return lambda str: _normalize(
        {key: priors[key] * markovs[key](str) for key in priors}
    )


default_classifier = classifier(
    {"en": 10.58, "es": 5.47, "fr": 4.07, "pt": 3.54, "de": 1.74}
)  # Source: https://journal.lib.uoguelph.ca/index.php/perj/article/view/826/1358
