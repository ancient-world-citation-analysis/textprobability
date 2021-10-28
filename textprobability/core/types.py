"""This module is not only a utility for accessing common types, but an index of the
important abstractions as well. Abbreviations such as "scp", "mpf", and "clf" may refer
to types defined here.
"""

from typing import Callable, Dict, Iterable, Sequence, Optional, Tuple

# -------------------------------------------------------------------------------------#
# The following are elemental types.                                                   |
# -------------------------------------------------------------------------------------#

Probability = float
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
Lexicon = Dict[Unit, Probability]
ContextLexicon = Dict[NGram, Lexicon]

# -------------------------------------------------------------------------------------#
# The following are more complicated types that require reusable implementations.      |
# -------------------------------------------------------------------------------------#

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
