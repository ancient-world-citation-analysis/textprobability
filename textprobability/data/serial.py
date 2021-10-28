"""This module provides serialization and deserialization utils."""

from typing import Any, Dict, Iterator, Tuple, Union
from textprobability.core.types import ContextLexicon, Lexicon, NGram
import json

# Recursive type annotations are needed here, but they are not supported.
Trie = Dict[str, Any]


def context_lexicon2trie(cl: ContextLexicon) -> Trie:
    """Converts a ContextLexicon to a Trie."""
    ret: Dict[str, Any] = {}
    for key in cl:
        current = ret
        for element in key[:-1]:
            if element not in current:
                current[element] = {}
            current = current[element]
        current[key[-1]] = cl[key]
    return ret


def trie2context_lexicon(trie: Trie) -> ContextLexicon:
    """Converts a Trie like the output of context_lexicon2trie to a ContextLexicon."""

    def tups(trie: Union[Trie, float], parents: NGram) -> Iterator[Tuple[NGram, float]]:
        if isinstance(trie, float):
            yield parents, trie
        else:
            for key in trie:
                yield from tups(trie[key], (*parents, key))

    ret: ContextLexicon = {}
    for parents, frequency in tups(trie, ()):
        ngram = parents[: len(parents) - 1]
        if ngram not in ret:
            ret[ngram] = {}
        lexicon: Lexicon = ret[ngram]
        lexicon[parents[-1]] = frequency
    return ret
