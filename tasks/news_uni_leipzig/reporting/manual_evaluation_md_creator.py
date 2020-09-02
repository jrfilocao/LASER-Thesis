from common.database_connector import get_database_connection
from common.sentence_repository import get_sentences_from_article
from reporting.manual_evaluation_repository import *
from reporting.md_writer import write_articles_into_md_file


def _build_article_pairs_and_write_to_file(file_name, article_pairs, database_cursor):
    for source_article_id, target_article_id in article_pairs:
        matched_sentence_pairs = get_matched_sentence_pairs_by_article_ids(source_article_id, target_article_id, database_cursor)
        named_entities = get_named_entities_by_article_ids(source_article_id, target_article_id, database_cursor)
        source_sentences = get_sentences_from_article(source_article_id, database_cursor)
        target_sentences = get_sentences_from_article(target_article_id, database_cursor)
        write_articles_into_md_file(file_name,
                                    source_sentences,
                                    target_sentences,
                                    source_article_id,
                                    target_article_id,
                                    matched_sentence_pairs,
                                    named_entities)


if __name__ == "__main__":
    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        for source_language, target_language in [('en', 'de'), ('en', 'pt'), ('de', 'pt')]:
            and_pairs = get_false_positive_article_pairs_and(source_language, target_language, database_cursor)
            file_name = 'output/{}_{}_article_pairs_and.md'.format(source_language, target_language)
            _build_article_pairs_and_write_to_file(file_name, and_pairs, database_cursor)

            or_pairs = get_false_positive_article_pairs_or(source_language, target_language, database_cursor)
            file_name = 'output/{}_{}_article_pairs_or.md'.format(source_language, target_language)
            _build_article_pairs_and_write_to_file(file_name, or_pairs, database_cursor)

            only_pairs = get_false_positive_article_pairs_only(source_language, target_language, database_cursor)
            file_name = 'output/{}_{}_article_pairs_only.md'.format(source_language, target_language)
            _build_article_pairs_and_write_to_file(file_name, only_pairs, database_cursor)

    finally:
        if database_connection is not None:
            database_connection.close()