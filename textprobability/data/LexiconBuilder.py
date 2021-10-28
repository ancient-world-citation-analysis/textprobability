"""Defines the LexiconBuilder, a class for accumulating data about a lexicon."""

from typing import Any, Dict
from textprobability.core.types import (
    Lexicon,
    ContextLexicon,
    Splitter,
    Text,
    Unit,
    NGram,
)

Counts = Dict[Unit, int]


class LexiconBuilder:
    """Accumulates data about a Lexicon."""

    def __init__(self, splitter: Splitter):
        """Initializes the builder to count linguistic units of the type output by
        `splitter`.
        :param splitter: the Splitter instance that determines the type of linguistic
        unit counted by `self`
        """
        self.splitter: Splitter = splitter
        self._counts: Counts = {}
        self.total = 0

    def add(self, text: Text):
        """Acquires information from `text`."""
        for unit in self.splitter(text):
            self._counts[unit] = self._counts.get(unit, 0) + 1
            self.total += 1

    def __getattr__(self, name: str) -> Any:
        if name == "lexicon":
            ret: Lexicon = {k: v / self.total for k, v in self._counts.items()}
            return ret
        raise AttributeError(
            "{} is not an attribute of this {} instance.".format(name, "LexiconBuilder")
        )


class LexiconContextLexiconBuilder(LexiconBuilder):
    """Accumulates data about a Lexicon and ContextLexicon."""

    def __init__(self, splitter: Splitter, n):
        """Initializes the builder to count linguistic units of the type output by
        `splitter`.
        :param splitter: the Splitter instance that determines the type of linguistic
        unit counted by `self`
        :param n: the number of preceding linguistic units used as context
        """
        self.n = n
        self._builders: Dict[NGram, LexiconBuilder] = {}
        super().__init__(splitter)

    def add(self, text: Text):
        sequence = self.splitter(text)
        for n_plus_one_gram in zip(*[sequence[start:] for start in range(self.n + 1)]):
            ngram = n_plus_one_gram[: self.n]
            self._builders[ngram] = self._builders.get(
                ngram, LexiconBuilder(self.splitter)
            )
            self._builders[ngram].add(n_plus_one_gram[-1])
        super().add(text)

    def __getattr__(self, name: str) -> Any:
        if name == "context_lexicon":
            ret: ContextLexicon = {
                key: self._builders[key].lexicon for key in self._builders
            }
            return ret
        return super().__getattr__(name)
