#!/usr/bin/python3


def _get_sentence_id(article_index, sentence_index, input_file_name):
    return str(input_file_name) + '_article_' + str(article_index) + '_sentence_' + str(sentence_index)


def _get_id_sentence_pair(sentence, sentence_id):
    return sentence_id + '    ' + sentence + '\n'


def write_id_sentence_pair_to_file(output_file, article_index, sentence, sentence_index, input_file_name):
    sentence_id = _get_sentence_id(article_index, sentence_index, input_file_name)
    id_sentence_pair = _get_id_sentence_pair(sentence, sentence_id)
    output_file.write(id_sentence_pair)


def _get_sentence_id_line(sentence_id):
    return sentence_id + '\n'


def write_sentence_id_to_file(output_file, article_index, sentence_index, input_file_name):
    sentence_id = _get_sentence_id(article_index, sentence_index, input_file_name)
    sentence_id_line = _get_sentence_id_line(sentence_id)
    output_file.write(sentence_id_line)


def _get_sentence_line(sentence):
    return sentence + '\n'


def write_sentence_to_file(output_file, sentence):
    sentence_line = _get_sentence_line(sentence)
    output_file.write(sentence_line)