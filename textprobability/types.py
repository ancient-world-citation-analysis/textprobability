"""This module is not only a utility for accessing common types, but an index of the
important abstractions as well. Abbreviations such as "scp", "mpf", and "clf" may refer
to types defined here.
"""

from typing import Callable, Dict, Iterable, Sequence, Optional, Tuple

# The following are elemental types.

Unit = str  # This is an abbreviation for "linguistic unit."
Text = Unit
Token = Unit
Char = Unit
NGram = Tuple[Unit]
Probability = float
Lexicon = Dict[Unit, Probability]
ContextLexicon = Dict[NGram, Lexicon]
# A given probability function may be undefined for certain inputs.
P = Callable[[str], Optional[Probability]]

# The following are more complicated types that must be implemented.

# See splitters.py for implementation.
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
# See lexicon for implementation(s).
# Iterable is used instead of Sequence here to allow constant-space iteration over a
# very large corpus.
LexiconFactory = Callable[[Iterable[Text], Splitter], Lexicon]
ContextLexiconFactory = Callable[[Iterable[Text], Splitter], ContextLexicon]
