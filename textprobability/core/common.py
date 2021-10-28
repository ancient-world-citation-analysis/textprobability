"""This module implements the basic, non-opinionated types of which there is only one
obvious implementation. See types.py for documentation.
"""

from textprobability.types import Collapser, CompoundPFactory, StatelessPFactory
from functools import reduce

collapser: Collapser = lambda scp, splitter: lambda string: reduce(
    lambda a, b: a * b if a is not None and b is not None else None,
    scp(splitter(string)),
    1,
)

cpf: CompoundPFactory = lambda scp1, scp2, scp3, splitter: (
    lambda p2: lambda sequence: [
        None
        if prob3 is None
        else (p2(unit) * (1 - prob3) if prob1 is None else prob1 * prob3)
        for prob1, prob3, unit in zip(scp1(sequence), scp3(sequence), sequence)
    ]
)(collapser(scp2, splitter))

spf: StatelessPFactory = lambda lexicon: lambda sequence: [
    lexicon.get(unit, None) for unit in sequence
]
