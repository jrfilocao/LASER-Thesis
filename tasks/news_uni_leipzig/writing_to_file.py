#!/usr/bin/python3


def _get_sentence_id(base_sentence_id, article_index, sentence_index):
    return base_sentence_id + '_article_' + str(article_index) + '_sentence_' + str(sentence_index)


def _get_id_sentence_pair(sentence, sentence_id):
    return sentence_id + '    ' + sentence + '\n'


def _get_id_sentence_file_name(input_file_name):
    return input_file_name + '_ids_sentences'


def write_id_sentence_pair_to_file(input_file_name, article_index, sentence, sentence_index):
    id_sentence_file_name = _get_id_sentence_file_name(input_file_name)

    with open(id_sentence_file_name, 'a') as id_sentence_file:
        sentence_id = _get_sentence_id(input_file_name, article_index, sentence_index)
        id_sentence_pair = _get_id_sentence_pair(sentence, sentence_id)
        id_sentence_file.write(id_sentence_pair)


def _get_ids_file_name(input_file_name):
    return input_file_name + '_ids'


def _get_sentence_id_line(sentence_id):
    return sentence_id + '\n'


def write_sentence_id_to_file(input_file_name, article_index, sentence_index):
    ids_file_name = _get_ids_file_name(input_file_name)

    with open(ids_file_name, 'a') as ids_file:
        sentence_id = _get_sentence_id(input_file_name, article_index, sentence_index)
        sentence_id_line = _get_sentence_id_line(sentence_id)
        ids_file.write(sentence_id_line)


def _get_sentences_file_name(input_file_name):
    return input_file_name + '_sentences'


def _get_sentence_line(sentence):
    return sentence + '\n'


def write_sentence_to_file(input_file_name, sentence):
    sentences_file_name = _get_sentences_file_name(input_file_name)

    with open(sentences_file_name, 'a') as sentences_file:
        sentence_line = _get_sentence_line(sentence)
        sentences_file.write(sentence_line)