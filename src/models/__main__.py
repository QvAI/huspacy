import logging
from os import path
from pprint import pprint

import click
import spacy
from gensim.models.keyedvectors import KeyedVectors

logging.basicConfig(level=logging.INFO)

RESOURCES_ROOT = path.abspath(path.join(path.dirname(__file__), "..", "resources"))


@click.group()
def cli():
    pass


@cli.command()
@click.argument("from_path")
@click.argument("to_path")
def convert_vectors_to_txt(from_path, to_path):
    model = KeyedVectors.load_word2vec_format(
        from_path, binary=True, unicode_errors="replace"
    )
    model.save_word2vec_format(to_path, binary=False)


@cli.command()
@click.argument("vectors_path")
def eval_vectors(vectors_path):
    model = KeyedVectors.load_word2vec_format(
        vectors_path, binary=not vectors_path.endswith(".txt"), unicode_errors="replace"
    )
    analogies_result = model.wv.evaluate_word_analogies(
        path.join(RESOURCES_ROOT, "questions-words-hu.txt"),
        dummy4unknown=True,
        restrict_vocab=None,
        case_insensitive=False
    )
    pprint(analogies_result[0])


@cli.command()
@click.argument("model_path")
def test_model(model_path):
    nlp = spacy.load(model_path)
    # FIXME: Why "Ez" is not a stopword?
    doc = nlp("Ez egy ház.")
    pprint(
        [
            dict(
                text=t.text,
                lemma=t.lemma_,
                pos=t.pos_,
                tag=t.tag_,
                dep=t.dep_,
                head=t.head,
                is_stop=t.is_stop,
                has_vector=t.has_vector,
                brown_cluser=t.cluster,
                prob=t.prob,
            )
            for t in doc
        ]
    )


if __name__ == "__main__":
    cli()
