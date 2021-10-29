"""This module implements the basic, non-opinionated types of which there is only one
obvious implementation. See types.py for documentation.
"""

from functools import reduce
from typing import cast, Optional, Callable

from textprobability.core.types import Collapser, CompoundPFactory, StatelessPFactory

_safe_mul: Callable[[Optional[float], Optional[float]], Optional[float]] = (
    lambda a, b: a * b if a is not None and b is not None else None
)

collapser: Collapser = lambda scp, splitter: lambda string: reduce(
    _safe_mul, scp(splitter(string)), cast(Optional[float], 1)
)

cpf: CompoundPFactory = lambda scp1, scp2, scp3, splitter: (
    lambda p2: lambda sequence: [
        None
        if prob3 is None
        else (_safe_mul(p2(unit), prob3) if prob1 is None else prob1 * (1 - prob3))
        for prob1, prob3, unit in zip(scp1(sequence), scp3(sequence), sequence)
    ]
)(collapser(scp2, splitter))

spf: StatelessPFactory = lambda lexicon: lambda sequence: [
    lexicon.get(unit, None) for unit in sequence
]
