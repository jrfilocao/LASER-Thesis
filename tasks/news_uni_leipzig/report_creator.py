from database_connector import get_database_connection
from report_repository import *
from report_writer import write_report_entries_into_csv_file


class ReportEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return self.key + ',' + self.value + '\n'

    def __str__(self):
        return self.key + ',' + self.value + '\n'


def create_report(sentence_pair_score_threshold, database_cursor):
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
    unique_article_pairs_with_common_named_entities_de_pt = get_unique_article_pairs_with_common_named_entities_de_pt(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt = \
        get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor)
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
    entries.append(ReportEntry('unique articles with more than 2 sentences de_pt', str(get_unique_articles_with_more_than_2_sentences_de_pt(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_en_pt_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('language', 'EN-PT'))
    entries.append(ReportEntry('sentence pairs en_pt', str(get_potential_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    unique_article_pairs_en_pt = get_unique_article_pairs_en_pt(sentence_pair_score_threshold, database_cursor)

    if unique_article_pairs_en_pt == 0:
        return
    unique_article_pairs_with_common_named_entities_en_pt = get_unique_article_pairs_with_common_named_entities_en_pt(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt = \
        get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor)
    unique_article_pairs_with_common_named_entities_en_pt_percentage = float(unique_article_pairs_with_common_named_entities_en_pt) / float(unique_article_pairs_en_pt) * 100
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt_percentage = \
        float(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt) / float(unique_article_pairs_en_pt) * 100
    entries.append(ReportEntry('unique article pairs en_pt', str(unique_article_pairs_en_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities en_pt', str(unique_article_pairs_with_common_named_entities_en_pt)))
    entries.append(ReportEntry('unique article pairs with common named entities en_pt percentage', str(unique_article_pairs_with_common_named_entities_en_pt_percentage)))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_pt',
                                      str(get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('unique articles with common named entities and multiple similar sentences en_pt percentage',
                                      str(unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt_percentage)))
    entries.append(ReportEntry('unique articles with more than 2 sentences en_pt', str(get_unique_articles_with_more_than_2_sentences_en_pt(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_en_de_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('language', 'EN-DE'))
    entries.append(ReportEntry('sentence pairs en_de', str(get_potential_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor))))
    unique_article_pairs_en_de = get_unique_article_pairs_en_de(sentence_pair_score_threshold, database_cursor)

    if unique_article_pairs_en_de == 0:
        return
    unique_article_pairs_with_common_named_entities_en_de = get_unique_article_pairs_with_common_named_entities_en_de(sentence_pair_score_threshold, database_cursor)
    unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de = \
        get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor)
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
    entries.append(ReportEntry('unique articles with more than 2 sentences en_de', str(get_unique_articles_with_more_than_2_sentences_en_de(sentence_pair_score_threshold, database_cursor))))
    return entries


def _get_total_report_entries(sentence_pair_score_threshold, database_cursor):
    entries = []
    entries.append(ReportEntry('total sentence pairs', str(get_total_sentence_pairs_count(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('total unique article pairs', str(get_total_unique_article_pairs_count(sentence_pair_score_threshold, database_cursor))))
    entries.append(ReportEntry('total unique article pairs with common named entities', str(get_total_unique_article_pairs_with_common_named_entities(sentence_pair_score_threshold, database_cursor))))
    total_unique_article_pairs_with_more_than_2_sentences = get_total_unique_article_pairs_with_more_than_2_sentences(sentence_pair_score_threshold, database_cursor)
    total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence = \
        get_total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence(sentence_pair_score_threshold, database_cursor)
    total_unique_article_pairs_with_common_named_entities_and_more_than_2_sentence = total_unique_article_pairs_with_more_than_2_sentences - total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence
    entries.append(ReportEntry('total unique article pairs with common named entities and more than 2 sentence', str(total_unique_article_pairs_with_common_named_entities_and_more_than_2_sentence)))
    entries.append(ReportEntry('total unique article pairs with more than 2 sentences', str(total_unique_article_pairs_with_more_than_2_sentences)))
    entries.append(ReportEntry('total unique article pairs without common named entities and with more than 2 sentence', str(total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence)))
    return entries


if __name__ == "__main__":

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        number_of_steps = 14
        threshold_step = 0.025
        sentence_pair_score_base_threshold = 0.8

        for i in range(number_of_steps):
            score_threshold = sentence_pair_score_base_threshold + i*threshold_step
            write_report_entries_into_csv_file(score_threshold, create_report(score_threshold, database_cursor))
    finally:
        if database_connection is not None:
            database_connection.close()
