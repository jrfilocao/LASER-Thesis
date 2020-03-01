#!/usr/bin/python3

from pyfasttext import FastText

import os
import sys
assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'
NEWS_TASK = os.environ['NEWS_TASK']
sys.path.append(NEWS_TASK + '/extraction')

MODEL = FastText(os.path.join(os.path.dirname(__file__), 'lid.176.ftz'))


def is_sentence_language_not_correct(sentence: str, language: str):
    prediction = MODEL.predict_proba_single(sentence, k=1)
    if len(prediction) == 0 or len(prediction[0]) == 0:
        return False
    return prediction[0][0] != language