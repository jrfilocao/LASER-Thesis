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
from report_entry import ReportEntry


def _create_statistics_report(sentence_pair_score_threshold, database_cursor):
    report_entries = []

    total_report_entries = _get_total_report_entries(sentence_pair_score_threshold, database_cursor)
    if total_report_entries is not None:
        report_entries.extend(total_report_entries)

    en_de_report_entries = _get_en_de_report_entries(sentence_pair_score_threshold, database_cursor)
    if en_de_report_entries is not None:
        report_entries.extend(en_de_report_entries)

    en_pt_report_entries = _get_en_pt_report_entries(sentence_pair_score_threshold, database_cursor)
    if en_pt_report_entries is not None:
        report_entries.extend(en_pt_report_entries)

    de_pt_report_entries = _get_de_pt_report_entries(sentence_pair_score_threshold, database_cursor)
    if de_pt_report_entries is not None:
        report_entries.extend(de_pt_report_entries)

    return report_entries


def _get_de_pt_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('language', 'DE-PT'))
    entries.append(ReportEntry('sentence pairs de_pt', str(get_potential_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor))))
    unique_article_pairs_de_pt = get_unique_article_pairs_de_pt(sentence_pair_score_threshold, database_cursor)

    if unique_article_pairs_de_pt == 0:
        return
    unique_article_pairs_with_common_named_entities_de_pt = get_unique_article_pairs_count_with_common_named_entities_de_pt(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt = \
        get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor)
    unique_article_pairs_with_common_named_entities_de_pt_percentage = float(unique_article_pairs_with_common_named_entities_de_pt) / float(unique_article_pairs_de_pt) * 100
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt_percentage = \
        float(unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt) / float(unique_article_pairs_de_pt) * 100
    entries.append(ReportEntry('unique article pairs de_pt', str(unique_article_pairs_de_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities de_pt', str(unique_article_pairs_with_common_named_entities_de_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities de_pt percentage', str(unique_article_pairs_with_common_named_entities_de_pt_percentage)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences de_pt',
                               str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences de_pt percentage',
                               str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt_percentage)))
    entries.append(
        ReportEntry('unique articles with more than 2 sentences de_pt', str(get_unique_articles_with_more_than_2_sentences_de_pt(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_en_pt_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('language', 'EN-PT'))
    entries.append(ReportEntry('sentence pairs en_pt', str(get_potential_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    unique_article_pairs_en_pt = get_unique_article_pairs_en_pt(sentence_pair_score_threshold, database_cursor)

    if unique_article_pairs_en_pt == 0:
        return
    unique_article_pairs_with_common_named_entities_en_pt = get_unique_article_pairs_count_with_common_named_entities_en_pt(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt = \
        get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor)
    unique_article_pairs_with_common_named_entities_en_pt_percentage = float(unique_article_pairs_with_common_named_entities_en_pt) / float(unique_article_pairs_en_pt) * 100
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt_percentage = \
        float(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt) / float(unique_article_pairs_en_pt) * 100
    entries.append(ReportEntry('unique article pairs en_pt', str(unique_article_pairs_en_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities en_pt', str(unique_article_pairs_with_common_named_entities_en_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities en_pt percentage', str(unique_article_pairs_with_common_named_entities_en_pt_percentage)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_pt',
                               str(get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_pt percentage',
                               str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt_percentage)))
    entries.append(
        ReportEntry('unique articles with more than 2 sentences en_pt', str(get_unique_articles_with_more_than_2_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_en_de_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('language', 'EN-DE'))
    entries.append(ReportEntry('sentence pairs en_de', str(get_potential_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor))))
    unique_article_pairs_en_de = get_unique_article_pairs_en_de(sentence_pair_score_threshold, database_cursor)

    if unique_article_pairs_en_de == 0:
        return
    unique_article_pairs_with_common_named_entities_en_de = get_unique_article_pairs_count_with_common_named_entities_en_de(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de = \
        get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor)
    unique_article_pairs_with_common_named_entities_en_de_percentage = float(unique_article_pairs_with_common_named_entities_en_de) / float(unique_article_pairs_en_de) * 100
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de_percentage = \
        float(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de) / float(unique_article_pairs_en_de) * 100
    entries.append(ReportEntry('unique article pairs en_de', str(unique_article_pairs_en_de)))
    entries.append(ReportEntry('unique article pairs with common named entities en_de', str(unique_article_pairs_with_common_named_entities_en_de)))
    entries.append(ReportEntry('unique article pairs with common named entities en_de percentage', str(unique_article_pairs_with_common_named_entities_en_de_percentage)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_de',
                               str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_de percentage',
                               str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de_percentage)))
    entries.append(
        ReportEntry('unique articles with more than 2 sentences en_de', str(get_unique_articles_with_more_than_2_sentences_en_de(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_total_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('total sentence pairs', str(get_total_sentence_pairs_count(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('total unique article pairs', str(get_total_unique_article_pairs_count(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('total unique article pairs with common named entities',
                               str(get_total_unique_article_pairs_with_common_named_entities(sentence_pair_score_threshold, database_cursor))))
    total_unique_article_pairs_with_more_than_2_sentences = get_total_unique_article_pairs_with_more_than_2_sentences(sentence_pair_score_threshold, database_cursor)
    total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence = \
        get_total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence(sentence_pair_score_threshold, database_cursor)
    total_unique_article_pairs_with_common_named_entities_and_more_than_2_sentence = total_unique_article_pairs_with_more_than_2_sentences - total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence
    entries.append(ReportEntry('total unique article pairs with common named entities and more than 2 sentence',
                               str(total_unique_article_pairs_with_common_named_entities_and_more_than_2_sentence)))
    entries.append(ReportEntry('total unique article pairs with more than 2 sentences', str(total_unique_article_pairs_with_more_than_2_sentences)))
    entries.append(ReportEntry('total unique article pairs without common named entities and with more than 2 sentence',
                               str(total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence)))
    return entries


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Finding articles for all languages in crawled news texts')
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

        statistics_reports = {}
        for index in range(number_of_threshold_steps):
            score_threshold = sentence_pair_score_base_threshold + index * threshold_step_value
            statistics_report = _create_statistics_report(score_threshold, database_cursor)
            write_report_entries_into_csv_file(score_threshold,
                                               statistics_report,
                                               output_report_base_file_name)
            statistics_reports[score_threshold] = statistics_report
        print(statistics_reports)
        write_consolidate_statistics_diagram_into_file(statistics_reports, output_report_base_file_name)

    finally:
        if database_connection is not None:
            database_connection.close()
