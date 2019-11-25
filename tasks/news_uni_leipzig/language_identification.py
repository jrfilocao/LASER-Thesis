#!/usr/bin/python3

from fasttext import FastText

MODEL = FastText('lid.176.ftz')


def is_sentence_language_not_correct(sentence: str, language: str):
    prediction = MODEL.predict_proba_single(sentence, k=1)
    if len(prediction) == 0 or len(prediction[0]) == 0:
        return False
    return prediction[0][0] != language