from typing import List

import pytest
from spacy import Language
from spacy.lang.hu import Hungarian
from spacy.tokens import Doc


@pytest.fixture(scope="module")
def nlp():
    # noinspection PyUnresolvedReferences
    from huspacy import components

    nlp = Hungarian()
    nlp.add_pipe("hun_sentencizer")
    return nlp


@pytest.mark.parametrize("sentences", [
    ["Szia!", "Hogy vagy?"],
    ["Mizujs?", "Hogy vagy?"],
    ["Szia.", "Hogy vagy?"],
    ["\"Szia!\" - mondta.", "Hogy vagy?"],
    ["Szia!", "\"Hogy vagy?\""],
    ["(Szia!) - mondta.", "Hogy vagy?"],
    ["Szinte hihetetlen sebességgel robog az idő.", "A nemrég"],
    ["Szia!", "Jó estét, Magyarország! című műsor."]
])
def test_sentencizer(nlp: Language, sentences: List[str]):
    doc: Doc = nlp(" ".join(sentences))
    actual: List[str] = [str(sent) for sent in doc.sents]
    assert sentences == actual
