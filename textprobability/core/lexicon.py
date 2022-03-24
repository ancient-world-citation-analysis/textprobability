"""Implements a buildable, serializable, deserializable lexicon."""


from typing import Any, Dict, Iterator, Tuple, Union, Optional
from textprobability.core.types import (
    Unit,
    Probability,
    NGram,
    ContextLexicon,
    Splitter,
    Text,
    Lexicon,
)

SerializableLexicon = Tuple[Dict[Unit, int], int]
# Recursive type annotations are needed here, but they are not supported.
SerializableContextLexicon = Dict[str, Union[SerializableLexicon, Any]]


class LexiconImpl(Lexicon):
    """A Lexicon associates linguistic units with probabilities."""

    # A Lexicon is backed by a _Probabilities instance.

    def __init__(self, counts: Dict[Unit, int], n_obs: int):
        """This constructor should never be called from outside this module. In Java it
        would be private.
        """
        self._counts: Dict[Unit, int] = counts
        self._probabilities: Dict[Unit, float] = {
            k: v / n_obs for k, v in counts.items()
        }
        super().__init__(n_obs)

    def __getitem__(self, key: Unit) -> Probability:
        """Returns the probability associated with `key`."""
        return self._probabilities[key]

    def get(
        self, key: Unit, default: Optional[Probability] = None
    ) -> Optional[Probability]:
        return self._probabilities[key] if key in self._probabilities else default

    def summarize(self, min_n):
        """Summarizes this, reducing the amount of space required to store
        this.
        :param min_n: The minimum number of observations of a linguistic unit for
        it to be recorded as observed.
        :return: A summarized version of this.
        """
        filtered = {
            unit: count for unit, count in self._counts.items() if count >= min_n
        }
        # sum(filtered.values()) should be very close to self.n_obs for reasonably
        # chosen min_n, but it is recomputed here anyway.
        return LexiconImpl(filtered, sum(filtered.values()))

    def to_serializable(self) -> SerializableLexicon:
        """Gets a representation of `self` that can be serialized using JSON."""
        return (self._counts, self.n_obs)

    @classmethod
    def from_serializable(cls, serializable: SerializableLexicon) -> Any:
        """Retrieves a Lexicon from its serializable representation."""
        return cls(*serializable)


def context_lexicon2serializable(cl: ContextLexicon) -> SerializableContextLexicon:
    """Converts a ContextLexicon to a Trie."""
    ret: SerializableContextLexicon = {}
    for key in cl:
        current = ret
        for element in key[:-1]:
            if element not in current:
                current[element] = {}
            # The following is okay because it will only be a Lexicon at the very end.
            current = current[element]  # type: ignore
        # This is the very end where current[element] is finally a Lexicon rather than
        # a nested SerializableContextLexicon.
        current[key[-1]] = cl[key].to_serializable()
    return ret


def serializable2context_lexicon(trie: SerializableContextLexicon) -> ContextLexicon:
    """Converts a Trie like the output of context_lexicon2trie to a ContextLexicon."""

    def walk(
        trie: Union[SerializableContextLexicon, SerializableLexicon], parents: NGram
    ) -> Iterator[Tuple[NGram, SerializableLexicon]]:
        if not isinstance(trie, dict):  # This is brittle.
            yield parents, trie
        else:
            for key in trie:
                yield from walk(trie[key], (*parents, key))

    ret: ContextLexicon = {}
    for ngram, serializable_lexicon in walk(trie, ()):
        ret[ngram] = LexiconImpl.from_serializable(serializable_lexicon)
    return ret


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

    def get_lexicon(self) -> Lexicon:
        """Returns the Lexicon accumulated by `self`."""
        return LexiconImpl.from_serializable((self._counts, self.total))


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

    def get_context_lexicon(self) -> ContextLexicon:
        """Returns the ContextLexicon accumulated by `self`."""
        return {key: self._builders[key].get_lexicon() for key in self._builders}
