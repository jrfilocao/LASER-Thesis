from common.database_connector import get_database_connection
from common.sentence_repository import get_sentences_from_article
from reporting.manual_evaluation_repository import get_article_pairs_and
from reporting.md_writer import write_sentences_md_file

if __name__ == "__main__":

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        en_de_pairs = get_article_pairs_and('en', 'de', database_cursor)

        for source_article_id, target_article_id in en_de_pairs:
            source_sentences = get_sentences_from_article(source_article_id, database_cursor)
            target_sentences = get_sentences_from_article(target_article_id, database_cursor)
            write_sentences_md_file('output/en_de_article_pairs.md', source_sentences, target_sentences, source_article_id, target_article_id)

    finally:
        if database_connection is not None:
            database_connection.close()