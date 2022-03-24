import time
from textprobability.core.types import P

print("Loading language data from JSON...")
t0 = time.time()
from textprobability.core.defaults import stateless, markov

en_s: P = stateless("en")
fr_s: P = stateless("fr")
en_m: P = markov("en")
fr_m: P = markov("fr")

for s in [
    "the",
    "ou",
    "est",
    "de",
    "that are",
    "can be",
    "usually do not",
    "period of time",
]:
    print(
        "Stateless: en({})={:.2e},{}fr({})={:.2e}".format(  # type: ignore
            s, en_s(s), " " * (15 - len(s)), s, fr_s(s)
        )
    )
    print(
        "Markov:    en({})={:.2e},{}fr({})={:.2e}".format(  # type: ignore
            s, en_m(s), " " * (15 - len(s)), s, fr_m(s)
        )
    )
    print()
