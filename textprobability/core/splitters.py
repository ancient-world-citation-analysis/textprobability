"""This module implements common schemes for splitting strings into linguistic units."""

from textprobability.core.types import Splitter
import re


latin_tokens: Splitter = lambda s: [
    w for w in re.split(r"(?<=[^\w�])|(?=[^\w�])", s) if w.strip()
]
characters: Splitter = lambda s: s  # A string is an iterable of strings.
