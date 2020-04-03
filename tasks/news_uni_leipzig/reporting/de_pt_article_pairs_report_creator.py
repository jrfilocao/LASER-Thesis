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

NAMED_ENTITY_OR_MULTIPLE_SENTENCES = 'ner_or_multiple'

INVALID_NAMED_ENTITY_OR_MULTIPLE_SENTENCES = 'invalid_ner_or_multiple'

FALSE_NEGATIVES_NAMED_ENTITY_OR_MULTIPLE_SENTENCES = 'false_negatives_ner_or_multiple'

NAMED_ENTITY_AND_MULTIPLE_SENTENCES = 'ner_multiple'

INVALID_NAMED_ENTITY_AND_MULTIPLE_SENTENCES = 'invalid_ner_multiple'

FALSE_NEGATIVES_NAMED_ENTITY_AND_MULTIPLE_SENTENCES = 'false_negatives_ner_multiple'

ONLY_NAMED_ENTITY = 'ner'

INVALID_ONLY_NAMED_ENTITY = 'invalid_ner'

FALSE_NEGATIVES_ONLY_NAMED_ENTITY = 'false_negatives_ner'

F_MEASURE_ALPHA = 0.5


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


def _get_correct_article_pairs_count_and_errors_and_average_sentence_count(rows):
    correct_article_pairs_count = 0
    total_matched_sentence_count_in_correct_pairs = 0
    incorrect_article_pairs = []

    for row in rows:
        if row[0][3:] == row[1][3:]: # de-ep-11-06-23-008 == pt-ep-11-06-23-008
            correct_article_pairs_count += 1
            total_matched_sentence_count_in_correct_pairs += row[2]
        else:
            incorrect_article_pairs.append(row)

    average_matched_sentence_count_in_correct_pairs = total_matched_sentence_count_in_correct_pairs / correct_article_pairs_count
    return correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs


def create_de_pt_article_pairs_report(score_threshold, database_cursor, output_report_base_file_name, total_number_of_articles, total_number_of_sentences):
    report_entries = []
    only_named_entity_result_rows = get_unique_article_pairs_with_common_named_entities_de_pt(score_threshold, database_cursor)
    only_named_entity_correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs = \
        _get_correct_article_pairs_count_and_errors_and_average_sentence_count(only_named_entity_result_rows)

    write_article_pair_results_into_file(score_threshold,
                                         incorrect_article_pairs,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         INVALID_ONLY_NAMED_ENTITY)

    false_negative_de_articles_with_common_named_entities_rows = get_false_negative_de_articles_with_common_named_entities_de_pt(score_threshold, database_cursor)

    write_article_pair_results_into_file(score_threshold,
                                         false_negative_de_articles_with_common_named_entities_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         FALSE_NEGATIVES_ONLY_NAMED_ENTITY)

    write_article_pair_results_into_file(score_threshold,
                                         only_named_entity_result_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         ONLY_NAMED_ENTITY)

    only_named_entity_de_pt_recall = float(only_named_entity_correct_article_pairs_count)/float(total_number_of_articles/2)
    only_named_entity_de_pt_precision = float(only_named_entity_correct_article_pairs_count) / float(len(only_named_entity_result_rows))
    only_named_entity_de_pt_f_measure = 1/(F_MEASURE_ALPHA/only_named_entity_de_pt_precision + (1-F_MEASURE_ALPHA)/only_named_entity_de_pt_recall)

    report_entries.append(('number_of_articles_extracted_de_pt', total_number_of_articles))
    report_entries.append(('number_of_articles_extracted_per_language_de_pt', total_number_of_articles/2))
    report_entries.append(('average_number_of_sentences_per_article', total_number_of_sentences / total_number_of_articles))
    report_entries.append(('only_named_entity_de_pt_recall', only_named_entity_de_pt_recall*100))
    report_entries.append(('only_named_entity_de_pt_precision', only_named_entity_de_pt_precision*100))
    report_entries.append(('only_named_entity_de_pt_f1_measure', only_named_entity_de_pt_f_measure*100))

    report_entries.append(('only_named_entity_de_pt_invalid_pair_count', len(incorrect_article_pairs)))
    report_entries.append(('only_named_entity_de_pt_average_matched_sentence_count', average_matched_sentence_count_in_correct_pairs))


    named_entity_and_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(score_threshold,
                                                                                                                                          database_cursor)
    named_entity_and_multiple_sentences_correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs = \
        _get_correct_article_pairs_count_and_errors_and_average_sentence_count(named_entity_and_multiple_sentences_result_rows)

    write_article_pair_results_into_file(score_threshold,
                                         incorrect_article_pairs,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         INVALID_NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

    false_negative_de_articles_with_common_named_entities_and_multiple_similar_sentences_rows = \
        get_false_negative_de_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(score_threshold, database_cursor)

    write_article_pair_results_into_file(score_threshold,
                                         false_negative_de_articles_with_common_named_entities_and_multiple_similar_sentences_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         FALSE_NEGATIVES_NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

    write_article_pair_results_into_file(score_threshold,
                                         named_entity_and_multiple_sentences_result_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

    named_entity_and_multiple_sentences_de_pt_recall = float(named_entity_and_multiple_sentences_correct_article_pairs_count) / float(total_number_of_articles/2)
    named_entity_and_multiple_sentences_de_pt_precision = float(named_entity_and_multiple_sentences_correct_article_pairs_count) / float(len(named_entity_and_multiple_sentences_result_rows))
    named_entity_and_multiple_sentences_de_pt_f_measure = 1/(F_MEASURE_ALPHA/named_entity_and_multiple_sentences_de_pt_precision + (1-F_MEASURE_ALPHA)/named_entity_and_multiple_sentences_de_pt_recall)

    report_entries.append(('named_entity_and_multiple_sentences_de_pt_recall', named_entity_and_multiple_sentences_de_pt_recall*100))
    report_entries.append(('named_entity_and_multiple_sentences_de_pt_precision', named_entity_and_multiple_sentences_de_pt_precision*100))
    report_entries.append(('named_entity_and_multiple_sentences_de_pt_f1_measure', named_entity_and_multiple_sentences_de_pt_f_measure*100))

    report_entries.append(('named_entity_and_multiple_sentences_de_pt_invalid_pair_count', len(incorrect_article_pairs)))
    report_entries.append(('named_entity_and_multiple_sentences_de_pt_average_matched_sentence_count', average_matched_sentence_count_in_correct_pairs))

    named_entity_or_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_or_multiple_similar_sentences_de_pt(score_threshold,
                                                                                                                                        database_cursor)
    named_entity_or_multiple_sentences_correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs = \
        _get_correct_article_pairs_count_and_errors_and_average_sentence_count(named_entity_or_multiple_sentences_result_rows)

    write_article_pair_results_into_file(score_threshold,
                                         incorrect_article_pairs,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         INVALID_NAMED_ENTITY_OR_MULTIPLE_SENTENCES)

    false_negative_de_articles_with_common_named_entities_or_multiple_similar_sentences_rows = \
        get_false_negative_de_articles_with_common_named_entities_or_multiple_similar_sentences_de_pt(score_threshold, database_cursor)

    write_article_pair_results_into_file(score_threshold,
                                         false_negative_de_articles_with_common_named_entities_or_multiple_similar_sentences_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         FALSE_NEGATIVES_NAMED_ENTITY_OR_MULTIPLE_SENTENCES)

    write_article_pair_results_into_file(score_threshold,
                                         named_entity_or_multiple_sentences_result_rows,
                                         output_report_base_file_name,
                                         GERMAN_PORTUGUESE,
                                         NAMED_ENTITY_OR_MULTIPLE_SENTENCES)

    named_entity_or_multiple_sentences_de_pt_recall = float(named_entity_or_multiple_sentences_correct_article_pairs_count) / float(total_number_of_articles/2)
    named_entity_or_multiple_sentences_de_pt_precision = float(named_entity_or_multiple_sentences_correct_article_pairs_count) / float(len(named_entity_or_multiple_sentences_result_rows))
    named_entity_or_multiple_sentences_de_pt_f_measure = 1/(F_MEASURE_ALPHA/named_entity_or_multiple_sentences_de_pt_precision + (1-F_MEASURE_ALPHA)/named_entity_or_multiple_sentences_de_pt_recall)

    report_entries.append(('named_entity_or_multiple_sentences_de_pt_recall', named_entity_or_multiple_sentences_de_pt_recall*100))
    report_entries.append(('named_entity_or_multiple_sentences_de_pt_precision', named_entity_or_multiple_sentences_de_pt_precision*100))
    report_entries.append(('named_entity_or_multiple_sentences_de_pt_f1_measure', named_entity_or_multiple_sentences_de_pt_f_measure*100))

    report_entries.append(('named_entity_or_multiple_sentences_de_pt_invalid_pair_count', len(incorrect_article_pairs)))
    report_entries.append(('named_entity_or_multiple_sentences_de_pt_average_matched_sentence_count', average_matched_sentence_count_in_correct_pairs))

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
            statistics_report = create_de_pt_article_pairs_report(score_threshold,
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
