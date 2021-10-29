"""This module is not only a utility for accessing common types, but an index of the
important abstractions as well. Abbreviations such as "scp", "mpf", and "clf" may refer
to types defined here.
"""

from typing import Callable, Dict, Iterable, Sequence, Optional, Tuple, Any

# -------------------------------------------------------------------------------------#
# The following are elemental types.                                                   |
# -------------------------------------------------------------------------------------#

Probability = float  # (In the interval [0, 1], of course.)
# A given probability function may be undefined for certain inputs.
P = Callable[[str], Optional[Probability]]
Unit = str  # This is an abbreviation for "linguistic unit."
Char = Unit
Token = Unit
Text = Unit
NGram = Tuple[Unit, ...]
# Iterable is used instead of Sequence here so that a large corpus need not be stored in
# memory.
Corpus = Iterable[Text]

# -------------------------------------------------------------------------------------#
# The following are more complicated types that require reusable implementations.      |
# -------------------------------------------------------------------------------------#


class Serializable:
    def to_serializable(self) -> Any:
        raise NotImplementedError()

    @classmethod
    def from_serializable(cls, serializable: Any) -> Any:
        raise NotImplementedError()


# See lexicon.py for implementation.
class Lexicon(Serializable):
    def __init__(self, n_obs: int):
        self.n_obs = n_obs

    def __getitem__(self, key: Unit) -> Probability:
        raise NotImplementedError()

    def get(
        self, key: Unit, default: Optional[Probability] = None
    ) -> Optional[Probability]:
        raise NotImplementedError()


ContextLexicon = Dict[NGram, Lexicon]
# See splitters.py for implementation.
# Splitters are idempotent.
Splitter = Callable[[str], Sequence[Unit]]
SequentialConditionalP = Callable[[Sequence[Unit]], Sequence[Optional[Probability]]]
# See common.py for implementation.
Collapser = Callable[[SequentialConditionalP, Splitter], P]
# See common.py for implementation.
StatelessPFactory = Callable[[Lexicon], SequentialConditionalP]
# See mpf for implementation(s).
MarkovPFactory = Callable[[ContextLexicon], SequentialConditionalP]
# See common.py for implementation.
# With a probability given by SCP3, any given Unit may be assigned undefined probability
# by SCP1, in which case that Unit is split using a Splitter into smaller Units that can
# be used as input to SCP2. SCP2 can then assign probability to that Unit.
# Note: Arbitrarily extended compounding is possible because any SCP may itself be
# a CompoundP.
CompoundPFactory = Callable[
    [SequentialConditionalP, SequentialConditionalP, SequentialConditionalP, Splitter],
    SequentialConditionalP,
]
# See common.py for implementation(s).
LexiconFactory = Callable[[Corpus, Splitter], Tuple[Lexicon, ContextLexicon]]
