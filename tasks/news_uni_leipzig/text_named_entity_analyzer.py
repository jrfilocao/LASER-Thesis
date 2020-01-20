#!/usr/bin/python3

import spacy
from spacy import displacy
import pt_core_news_sm
import de_core_news_sm
import en_core_web_sm
from fuzzywuzzy import fuzz, process

NAMED_ENTITY_MINIMUM_LENGTH = 3
TOKEN_SORT_RATIO_THRESHOLD = 70

NLP_PT = pt_core_news_sm.load()
NLP_DE = de_core_news_sm.load()
NLP_EN = en_core_web_sm.load()

MODELS = {'de': NLP_DE,
          'en': NLP_EN,
          'pt': NLP_PT,
          }


def _get_nlp_model(language):
    return MODELS[language]


def _get_named_entities(text, language):
    nlp_model = _get_nlp_model(language)
    named_entities = nlp_model(text).ents
    return named_entities


def _is_named_entity_longer_than_minimum(named_entity_text):
    return len(named_entity_text) >= NAMED_ENTITY_MINIMUM_LENGTH


def _is_similar_named_entities(source_named_entity_text, target_named_entity_text, token_sort_ratio):
    if token_sort_ratio > TOKEN_SORT_RATIO_THRESHOLD and \
            _is_named_entity_longer_than_minimum(source_named_entity_text) and \
            _is_named_entity_longer_than_minimum(target_named_entity_text):
        return True
    return False


def _get_similar_named_entities(source_named_entities, target_named_entities):
    similar_named_entities = set()
    for source_named_entity in source_named_entities:
        for target_named_entity in target_named_entities:
            token_sort_ratio = fuzz.token_sort_ratio(source_named_entity.text, target_named_entity.text)
            similar_named_entities_boolean = _is_similar_named_entities(source_named_entity.text, target_named_entity.text, token_sort_ratio)
            if similar_named_entities_boolean:
                similar_named_entities.add(SimilarNamedEntityPair(source_named_entity.text, target_named_entity.text, token_sort_ratio))
    return similar_named_entities


def get_similar_entities_in_crosslingual_texts(source_text, source_language, target_text, target_language):
    source_named_entities = _get_named_entities(source_text, source_language)
    target_named_entities = _get_named_entities(target_text, target_language)

    return _get_similar_named_entities(source_named_entities, target_named_entities)


class SimilarNamedEntityPair:
    def __init__(self, source_text, target_text, ratio):
        self.source_text = source_text
        self.target_text = target_text
        self.ratio = ratio

    def __repr__(self):
        return self.source_text + ' ' + self.target_text + ' ' + str(self.ratio)

    def __str__(self):
        return self.source_text + ' ' + self.target_text + ' ' + str(self.ratio)

    def __hash__(self):
        return hash((self.source_text, self.target_text, self.ratio))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.source_text == other.source_text and self.target_text == other.target_text and self.ratio == other.ratio
