#!/usr/bin/python3

EMPTY_STRING = ''
NEW_LINE = '\n'
DOT = '.'
INTERROGATION = '?'


def extract_single_article_from_file(input_file_name):
    with open(input_file_name, 'r', errors='replace') as input_file:

        article_sentences = []
        file_lines = input_file.readlines()

        for file_line in file_lines:
            sentence_without_new_line = file_line.replace(NEW_LINE, EMPTY_STRING)
            sentence_without_quote_signs = _remove_all_quote_signs(sentence_without_new_line)
            sentence_without_leading_spaces = sentence_without_quote_signs.strip()
            if not _is_meta_information_sentence:
                article_sentences.append(sentence_without_leading_spaces)

    return article_sentences


def _is_meta_information_sentence(sentence):
    last_character = sentence[-1:]
    return last_character == DOT or last_character == INTERROGATION


def _remove_all_quote_signs(text):
    return text.replace('“', '').replace('„', '').replace('"', '').replace('\'', ' ').replace('`', '');
