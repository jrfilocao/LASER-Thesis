#!/usr/bin/python3

EMPTY_STRING = ''
NEW_LINE = '\n'


def extract_single_article_from_file(input_file_name):
    with open(input_file_name, 'r', errors='replace') as input_file:

        article_sentences = []
        file_lines = input_file.readlines()

        for file_line in file_lines:
            sentence_with_no_new_line = file_line.replace(NEW_LINE, EMPTY_STRING)
            sentence_without_quote_signs = _remove_all_quote_signs(sentence_with_no_new_line)
            article_sentences.append(sentence_without_quote_signs)

    return article_sentences


def _remove_all_quote_signs(text):
    return text.replace('“', '').replace('„', '').replace('"', '').replace('\'', ' ');
