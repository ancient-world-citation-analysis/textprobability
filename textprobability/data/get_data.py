import json
import argparse
import sys
import time
from numpy.random import default_rng
from textprobability.core.splitters import latin_tokens, characters
from textprobability.data.serial import context_lexicon2serializable

from textprobability.data.web_walk import (
    web_walk,
    wikipedia,
    wikipedia_about_page,
    get_query_string_remover,
    get_prefixer,
)
from textprobability.data.LexiconBuilder import LexiconContextLexiconBuilder

_SECONDS_PER_HOUR = 60 * 60


def main(
    langcode: str,
    out: str,
    max_time: float,
    max_text: int,
    seed: int,
    token_n: int,
    char_n: int,
) -> int:
    token_builder = LexiconContextLexiconBuilder(latin_tokens, token_n)
    char_builder = LexiconContextLexiconBuilder(characters, char_n)
    t0 = time.time()

    def finish():
        with open(out, "w") as f:
            json.dump(
                {
                    "token_lexicon": token_builder.lexicon,
                    "token_context_lexicon": context_lexicon2serializable(
                        token_builder.context_lexicon
                    ),
                    "char_lexicon": char_builder.lexicon,
                    "char_context_lexicon": context_lexicon2serializable(
                        char_builder.context_lexicon
                    ),
                },
                f,
            )

    for text in web_walk(
        wikipedia_about_page(langcode),
        default_rng(seed),
        {wikipedia(langcode)},
        url_resolver=get_query_string_remover(get_prefixer(wikipedia(langcode))),
        verbose=True,
    ):
        if token_builder.total >= max_text and max_text != -1:
            finish()
            return 0
        if time.time() - t0 > max_time * _SECONDS_PER_HOUR:
            finish()
            return 0
        token_builder.add(text)
        char_builder.add(text)
    return 0


main("en", "en.json", 0.01, -1, 905, 1, 2)


"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script gets data about a given language and saves it."
    )
    parser.add_argument("langcode", help="The language code of the desired text.")
    parser.add_argument("out", help="The path to the output file.")
    parser.add_argument(
        "--max-time",
        default=float("inf"),
        help="The approximate maximum time this script can run, in hours.",
        type=float,
    )
    parser.add_argument(
        "--max-text",
        default=-1,
        help="The approximate maximum number of tokens to collect.",
        type=int,
    )
    parser.add_argument(
        "--seed",
        default=2319,
        help="The random seed that completely determines this program's behavior.",
        type=int,
    )
    parser.add_argument(
        "--token-n",
        default=1,
        help="The number of preceding tokens to consider as context.",
        type=int,
    )
    parser.add_argument(
        "--char-n",
        default=2,
        help="The number of preceding characters to consider as context.",
        type=int,
    )
    args = parser.parse_args()
    sys.exit(
        main(
            args.langcode,
            args.out,
            args.max_time,
            args.max_text,
            args.seed,
            args.token_n,
            args.char_n,
        )
    )
"""
