"""This module exports general-purpose utilities that should suffice for most use cases.
"""
from pathlib import Path
import json

from textprobability.core.types import SequentialConditionalP, P
from textprobability.core.common import cpf, spf, collapser
import textprobability.core.mpf as mpf
from textprobability.core.splitters import latin_tokens, characters
from textprobability.data.langdata import DefaultLangData


DEFAULT_DATA_PATH: Path = Path(__file__).parent.parent / "data"


def _get_data_latin(langcode: str, path: str) -> DefaultLangData:
    """Retrieves the language data associated with `langcode`."""
    # FIXME: This should be placed on sys.path so that there is no reliance on relative
    # paths. This is one of a number of changes that would be required to allow people
    # to install and interact with this.
    with open(Path(path) / "{}.json".format(langcode)) as f:
        return DefaultLangData.from_serializable(json.load(f))


def _constant_scp3(c: float) -> SequentialConditionalP:
    """Returns a simple SCP that can only ever return one probability."""
    return lambda sequence: [c for _ in range(len(sequence))]


def stateless(langcode: str, path=DEFAULT_DATA_PATH) -> P:
    """Returns the default stateless P for the given language."""
    data: DefaultLangData = _get_data_latin(langcode, path)
    token2char_scp3: SequentialConditionalP = _constant_scp3(
        1 / data.token_lexicon.n_obs
    )
    return collapser(
        cpf(
            spf(data.token_lexicon), spf(data.char_lexicon), token2char_scp3, characters
        ),
        latin_tokens,
    )


def markov(langcode: str, path=DEFAULT_DATA_PATH) -> P:
    """Returns the default markov P for the given language."""
    data: DefaultLangData = _get_data_latin(langcode, path)
    tokens2token_scp3: SequentialConditionalP = _constant_scp3(
        0.5  # FIXME: This is probably very wrong!
    )
    token2char_scp3: SequentialConditionalP = _constant_scp3(
        1 / data.token_lexicon.n_obs
    )
    chars2char_scp3: SequentialConditionalP = _constant_scp3(
        0.5  # FIXME: This is probably very wrong!
    )
    char2nothing_scp3: SequentialConditionalP = _constant_scp3(
        1 / data.char_lexicon.n_obs
    )
    return collapser(
        cpf(
            cpf(
                mpf.default(data.token_context_lexicon),
                spf(data.token_lexicon),
                tokens2token_scp3,
                latin_tokens,
            ),
            cpf(
                mpf.default(data.char_context_lexicon),
                cpf(
                    spf(data.char_lexicon),
                    _constant_scp3(1),
                    char2nothing_scp3,
                    characters,
                ),
                chars2char_scp3,
                latin_tokens,
            ),
            token2char_scp3,
            characters,
        ),
        latin_tokens,
    )
