#!/usr/bin/python3

from xml.dom import minidom

SENTENCE_TAG = 's'

EMPTY_STRING = ''
NEW_LINE = '\n'


def extract_single_article_from_file(input_file_name):
    xml_file = minidom.parse(input_file_name)
    sentences = xml_file.getElementsByTagName(SENTENCE_TAG)

    article_sentences = []
    for sentence in sentences:
        sentence_text = sentence.firstChild.data
        sentence_text_without_quote_signs = _remove_all_quote_signs(sentence_text)
        article_sentences.append(sentence_text_without_quote_signs)

    return article_sentences


def _remove_all_quote_signs(text):
    return text.replace('“', '').replace('„', '').replace('"', '').replace('\'', ' ');
