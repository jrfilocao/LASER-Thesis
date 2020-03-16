import argparse
import os
import sys
assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'
NEWS_TASK = os.environ['NEWS_TASK']
sys.path.append(NEWS_TASK + '/common')
sys.path.append(NEWS_TASK + '/reporting')

from database_connector import get_database_connection
from report_repository import *
from report_writer import *


GERMAN_PORTUGUESE = 'de_pt'

ENGLISH_PORTUGUESE = 'en_pt'

ENGLISH_GERMAN = 'en_de'

NAMED_ENTITY_AND_MULTIPLE_SENTENCES = 'ner_multiple'

INVALID_NAMED_ENTITY_AND_MULTIPLE_SENTENCES = 'invalid_ner_multiple'

ONLY_NAMED_ENTITY = 'ner'

INVALID_ONLY_NAMED_ENTITY = 'invalid_ner'


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Create found article pairs report')
    parser.add_argument('--number-of-threshold-steps', type=int, default=14,
                        help='number of threshold steps')
    parser.add_argument('--threshold-step-value', type=float, default=0.025,
                        help='threshold step value')
    parser.add_argument('--sentence-pair-score-base-threshold', type=float, default=0.8,
                        help='sentence pair score base threshold')
    parser.add_argument('--output-report-base-file-name', required=True, default='../output_files/report_pairs',
                        help='output report base file name')
    return parser


def _get_correct_article_pairs_count_and_errors_and_average_sentence_count(only_named_entity_result_rows):
    correct_article_pairs_count = 0
    total_matched_sentence_count_in_correct_pairs = 0
    incorrect_article_pairs = []

    for only_named_entity_result_row in only_named_entity_result_rows:
        if only_named_entity_result_row[0][3:] == only_named_entity_result_row[1][3:]: # de_1998_03_21_article_1 == en_1998_03_21_article_1
            correct_article_pairs_count += 1
            total_matched_sentence_count_in_correct_pairs += only_named_entity_result_row[2]
        else:
            incorrect_article_pairs.append(only_named_entity_result_row)

    average_matched_sentence_count_in_correct_pairs = total_matched_sentence_count_in_correct_pairs / correct_article_pairs_count
    return correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs


def create_en_de_article_pairs_report(score_threshold, database_cursor, output_report_base_file_name, total_number_of_articles, total_number_of_sentences):
    report_entries = []
    only_named_entity_result_rows = get_unique_article_pairs_with_common_named_entities_en_de(score_threshold, database_cursor)
    only_named_entity_correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs = \
        _get_correct_article_pairs_count_and_errors_and_average_sentence_count(only_named_entity_result_rows)

    write_article_pair_results_into_file(score_threshold,
                                         incorrect_article_pairs,
                                         output_report_base_file_name,
                                         ENGLISH_GERMAN,
                                         INVALID_ONLY_NAMED_ENTITY)

    report_entries.append(('number_of_articles_extracted_en_de', total_number_of_articles))
    report_entries.append(('number_of_articles_extracted_per_language_en_de', total_number_of_articles/2))
    report_entries.append(('average_number_of_sentences_per_article', total_number_of_sentences / total_number_of_articles))
    report_entries.append(('only_named_entity_en_de_recall', float(only_named_entity_correct_article_pairs_count)/float(total_number_of_articles/2)*100))
    report_entries.append(('only_named_entity_en_de_precision', float(only_named_entity_correct_article_pairs_count) / float(len(only_named_entity_result_rows)) * 100))
    report_entries.append(('only_named_entity_en_de_invalid_pair_count', len(incorrect_article_pairs)))
    report_entries.append(('only_named_entity_en_de_average_matched_sentence_count', average_matched_sentence_count_in_correct_pairs))

    write_article_pair_results_into_file(score_threshold,
                                         only_named_entity_result_rows,
                                         output_report_base_file_name,
                                         ENGLISH_GERMAN,
                                         ONLY_NAMED_ENTITY)
    named_entity_and_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(score_threshold,
                                                                                                                                          database_cursor)
    named_entity_and_multiple_sentences_correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs = \
        _get_correct_article_pairs_count_and_errors_and_average_sentence_count(named_entity_and_multiple_sentences_result_rows)

    write_article_pair_results_into_file(score_threshold,
                                         incorrect_article_pairs,
                                         output_report_base_file_name,
                                         ENGLISH_GERMAN,
                                         INVALID_NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

    report_entries.append(('named_entity_and_multiple_sentences_en_de_recall',
                          float(named_entity_and_multiple_sentences_correct_article_pairs_count) / float(total_number_of_articles/2) * 100))
    report_entries.append(('named_entity_and_multiple_sentences_en_de_precision',
                          float(named_entity_and_multiple_sentences_correct_article_pairs_count) / float(len(named_entity_and_multiple_sentences_result_rows)) * 100))
    report_entries.append(('named_entity_and_multiple_sentences_en_de_invalid_pair_count', len(incorrect_article_pairs)))
    report_entries.append(('named_entity_and_multiple_sentences_en_de_average_matched_sentence_count', average_matched_sentence_count_in_correct_pairs))

    write_article_pair_results_into_file(score_threshold,
                                         named_entity_and_multiple_sentences_result_rows,
                                         output_report_base_file_name,
                                         ENGLISH_GERMAN,
                                         NAMED_ENTITY_AND_MULTIPLE_SENTENCES)
    return report_entries



if __name__ == "__main__":

    parser = _get_argument_parser()
    arguments = parser.parse_args()

    output_report_base_file_name = arguments.output_report_base_file_name
    threshold_step_value = arguments.threshold_step_value
    sentence_pair_score_base_threshold = arguments.sentence_pair_score_base_threshold
    number_of_threshold_steps = arguments.number_of_threshold_steps

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        total_number_of_articles = get_total_number_of_articles(database_cursor)
        total_number_of_sentences = get_total_number_of_sentences(database_cursor)

        statistics_reports = {}
        for i in range(number_of_threshold_steps):
            score_threshold = sentence_pair_score_base_threshold + i * threshold_step_value
            statistics_report = create_en_de_article_pairs_report(score_threshold,
                                                                  database_cursor,
                                                                  output_report_base_file_name,
                                                                  total_number_of_articles,
                                                                  total_number_of_sentences)
            statistics_reports[score_threshold] = statistics_report

        print(statistics_reports)
        write_consolidate_statistics_diagram_into_file(statistics_reports, output_report_base_file_name)

    finally:
        if database_connection is not None:
            database_connection.close()
