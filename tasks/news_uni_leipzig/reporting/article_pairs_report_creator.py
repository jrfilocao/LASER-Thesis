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

ONLY_NAMED_ENTITY = 'ner'


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Create found article pairs report')
    parser.add_argument('--number-of-threshold-steps', type=int, default=14,
                        help='number of threshold steps')
    parser.add_argument('--threshold-step-value', type=float, default=0.025,
                        help='threshold step value')
    parser.add_argument('--sentence-pair-score-base-threshold', type=float, default=0.8,
                        help='sentence pair score base threshold')
    parser.add_argument('--output-report-base-file-name', required=True, default='../output_files/report',
                        help='output report base file name')
    return parser


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

        for i in range(number_of_threshold_steps):
            score_threshold = sentence_pair_score_base_threshold + i * threshold_step_value

            only_named_entity_en_de_result_rows = get_unique_article_pairs_with_common_named_entities_en_de(score_threshold, database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 only_named_entity_en_de_result_rows,
                                                 output_report_base_file_name,
                                                 ENGLISH_GERMAN,
                                                 ONLY_NAMED_ENTITY)

            named_entity_and_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(score_threshold,
                                                                                                                                                  database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 named_entity_and_multiple_sentences_result_rows,
                                                 output_report_base_file_name,
                                                 ENGLISH_GERMAN,
                                                 NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

            only_named_entity_en_pt_result_rows = get_unique_article_pairs_with_common_named_entities_en_pt(score_threshold, database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 only_named_entity_en_pt_result_rows,
                                                 output_report_base_file_name,
                                                 ENGLISH_PORTUGUESE,
                                                 ONLY_NAMED_ENTITY)

            named_entity_and_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(score_threshold,
                                                                                                                                                  database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 named_entity_and_multiple_sentences_result_rows,
                                                 output_report_base_file_name,
                                                 ENGLISH_PORTUGUESE,
                                                 NAMED_ENTITY_AND_MULTIPLE_SENTENCES)

            only_named_entity_de_pt_result_rows = get_unique_article_pairs_with_common_named_entities_de_pt(score_threshold, database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 only_named_entity_de_pt_result_rows,
                                                 output_report_base_file_name,
                                                 GERMAN_PORTUGUESE,
                                                 ONLY_NAMED_ENTITY)

            named_entity_and_multiple_sentences_result_rows = get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(score_threshold,
                                                                                                                                                  database_cursor)
            write_article_pair_results_into_file(score_threshold,
                                                 named_entity_and_multiple_sentences_result_rows,
                                                 output_report_base_file_name,
                                                 GERMAN_PORTUGUESE,
                                                 NAMED_ENTITY_AND_MULTIPLE_SENTENCES)
    finally:
        if database_connection is not None:
            database_connection.close()
