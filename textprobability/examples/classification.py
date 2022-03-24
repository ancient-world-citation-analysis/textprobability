snippets = [
    ("en", "IETF language tags were first"),
    ("en", "from Stesichorus"),
    ("en", "of 106,460,000 km2"),
    ("fr", "où le sigle désigne l'Internet Engineering Task Force"),
    ("fr", "du mot est"),
    ("fr", "donc"),
    ("es", '"en" denota al inglés'),
    ("es", "las riberas norteafricanas"),
    ("es", "La máxima"),
    ("de", "sondern jeder darf"),
    ("de", "das relativ"),
    ("de", "geht"),
    ("pt", "Seu nome deriva de Atlas"),
    ("pt", "ao calor"),
    ("pt", "tempo"),
]

import time

print("Loading language data from JSON...")
t0 = time.time()
from textprobability.classify import default_classifier

print(f"Loaded default classifier in {time.time() - t0:.1f} seconds.")


t0 = time.time()

for langcode, snippet in snippets:
    result = default_classifier(snippet)
    probabilities = "\n".join(
        f"    Pr({lang}) = {result[lang]:.7f}{' ✔' if lang == langcode else ''}"
        for lang in result
    )
    print(f'"{snippet}" (language: {langcode})\n{probabilities}')

print(f"Classified {len(snippets)} snippets in {time.time() - t0:.1f} seconds.")
