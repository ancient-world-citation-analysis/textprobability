"""This module is not only a utility for accessing common types, but an index of the
important abstractions as well."""

from typing import Callable, Dict, Sequence, Optional, Tuple

Unit = str  # This is an abbreviation for "linguistic unit."
Text = Unit
Token = Unit
Char = Unit
NGram = Tuple[Unit]

Splitter = Callable[[str], Sequence[Unit]]

Probability = float

Lexicon = Dict[Unit, float]
ContextLexicon = Dict[NGram, Lexicon]

# A given probability function may be undefined for certain inputs.
P = Callable[[str], Optional[Probability]]
SequentialConditionalP = Callable[[Sequence[Unit]], Sequence[Optional[Probability]]]

# A rough analogue of a splitter. It should be noted that given the semantics of the
# SequentialConditionalP type, there is only one Collapser implementation that will
# rhyme well with one's probabilistic intuition.
Collapser = Callable[[SequentialConditionalP], P]

StatelessPFactory = Callable[[Lexicon], SequentialConditionalP]
MarkovPFactory = Callable[[ContextLexicon], SequentialConditionalP]
# With a probability given by SCP3, any given Unit may be assigned undefined probability
# by SCP1, in which case that Unit is split using a Splitter into smaller Units that can
# be used as input to SCP2. SCP2 can then assign probability to that Unit.
# Note: Arbitrarily extended compounding is possible because any SCP may itself be
# a CompoundP.
# Note: Given the semantics of the CompoundPFactory type, there is only one
# CompoundPFactory implementation that will feel appropriate.
CompoundPFactory = Callable[
    [SequentialConditionalP, SequentialConditionalP, SequentialConditionalP, Splitter],
    SequentialConditionalP,
]

LexiconFactory = Callable[[Sequence[Text], Splitter], Lexicon]
ContextLexiconFactory = Callable[[Sequence[Text], Splitter], ContextLexicon]
