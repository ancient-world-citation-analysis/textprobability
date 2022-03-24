"""This module defines data structure types that comprehensively describe a program's
actionable knowledge about a given class of text.
"""

from typing import Any, cast

from textprobability.core.types import Lexicon, ContextLexicon, Serializable
from textprobability.core.lexicon import (
    LexiconImpl,
    context_lexicon2serializable,
    serializable2context_lexicon,
)


class DefaultLangData(Serializable):
    """Represents the default form taken by language data."""

    def __init__(
        self,
        token_lexicon: LexiconImpl,
        token_context_lexicon: ContextLexicon,
        char_lexicon: LexiconImpl,
        char_context_lexicon: ContextLexicon,
    ):
        self.token_lexicon = token_lexicon
        self.token_context_lexicon = token_context_lexicon
        self.char_lexicon = char_lexicon
        self.char_context_lexicon = char_context_lexicon

    def summarize(self, min_n=5) -> Any:
        """Summarizes this, reducing the amount of space required to store
        this.
        :param min_n: The minimum number of observations of a linguistic unit for
        it to be recorded as observed.
        :return: A summarized version of this.
        """
        return DefaultLangData(
            token_lexicon=self.token_lexicon.summarize(min_n),
            token_context_lexicon={
                ngram: cast(LexiconImpl, lexicon).summarize(min_n)
                for ngram, lexicon in self.token_context_lexicon.items()
                if lexicon.n_obs >= min_n
            },
            char_lexicon=self.char_lexicon.summarize(min_n),
            char_context_lexicon={
                ngram: cast(LexiconImpl, lexicon).summarize(min_n)
                for ngram, lexicon in self.char_context_lexicon.items()
                if lexicon.n_obs >= min_n
            },
        )

    def to_serializable(self) -> Any:
        return {
            "token_lexicon": self.token_lexicon.to_serializable(),
            "token_context_lexicon": context_lexicon2serializable(
                self.token_context_lexicon
            ),
            "char_lexicon": self.char_lexicon.to_serializable(),
            "char_context_lexicon": context_lexicon2serializable(
                self.char_context_lexicon
            ),
        }

    @classmethod
    def from_serializable(cls, serializable: Any) -> Any:
        return cls(
            LexiconImpl.from_serializable(serializable["token_lexicon"]),
            serializable2context_lexicon(serializable["token_context_lexicon"]),
            LexiconImpl.from_serializable(serializable["char_lexicon"]),
            serializable2context_lexicon(serializable["char_context_lexicon"]),
        )
