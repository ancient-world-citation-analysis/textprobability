"""This module provides MarkovPFactory implementations."""
from typing import cast, List, Optional

from textprobability.core.types import MarkovPFactory

default: MarkovPFactory = lambda cl: (
    lambda key_len: lambda sequence: cast(List[Optional[float]], [None] * key_len)
    + [
        cl[context].get(unit, None) if context in cl else None
        for context, unit in zip(
            zip(*[sequence[start:] for start in range(key_len)]), sequence[key_len:]
        )
    ]
)(len(next(iter(cl.keys()))))
