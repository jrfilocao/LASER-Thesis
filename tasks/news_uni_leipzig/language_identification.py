#!/usr/bin/python3

from pyfasttext import FastText

MODEL = FastText('lid.176.ftz')

def is_sentence_language_not_correct(sentence: str, language: str):
    prediction = MODEL.predict_proba_single(sentence, k=1)
    return prediction[0][0] != language