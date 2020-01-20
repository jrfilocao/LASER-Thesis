#!/usr/bin/python3


import argparse
from database_connector import get_database_connection
from sentence_repository import get_articles_from_sentence, get_sentences_from_article
from text_named_entity_analyzer import get_similar_entities_in_crosslingual_texts
from matched_article_repository import insert_matched_article


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Analysing article similarity through similar sentences')
    parser.add_argument('--sentence-candidate-file-paths', nargs='+', help='sentence candidate files to be analysed', required=True)
    parser.add_argument('--file-language-pairs', nargs='+', help='language of sentence candidates', required=True)
    return parser


def get_score_sentences_triple():
    score_sentences = sentence_candidate.split('\t')
    if len(score_sentences) == 3:
        for score_sentences_element in score_sentences:
            if not score_sentences_element.strip():
                raise ValueError
        return score_sentences[0].strip(), score_sentences[1].strip(), score_sentences[2].strip()
    raise ValueError


def _get_article_sentences_as_text(sentences):
    return " ".join(sentence_tuple[0] for sentence_tuple in sentences)


def _get_source_target_languages(file_language_pair):
    source_language, target_language = file_language_pair.split('_')
    return source_language, target_language


if __name__ == "__main__":
    parser = _get_argument_parser()
    arguments = parser.parse_args()

    # TODO add id_sentence_pair_persister
    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        for sentence_candidate_file_path, file_language_pair in zip(arguments.sentence_candidate_file_paths, arguments.file_language_pairs):
            with open(sentence_candidate_file_path, 'r') as  sentence_candidate_file:
                sentence_candidates = sentence_candidate_file.readlines()
                for sentence_candidate in sentence_candidates:
                    try:
                        score, source_sentence, target_sentence = get_score_sentences_triple()
                    except ValueError:
                        continue

                    source_article_id = get_articles_from_sentence(source_sentence, database_cursor)
                    target_article_id = get_articles_from_sentence(target_sentence, database_cursor)

                    source_article_sentences = get_sentences_from_article(source_article_id, database_cursor)
                    target_article_sentences = get_sentences_from_article(target_article_id, database_cursor)

                    source_article_text = _get_article_sentences_as_text(source_article_sentences)
                    target_article_text = _get_article_sentences_as_text(target_article_sentences)

                    source_language, target_language = _get_source_target_languages(file_language_pair)
                    similar_named_entities = get_similar_entities_in_crosslingual_texts(source_article_text,
                                                                                        source_language,
                                                                                        target_article_text,
                                                                                        target_language)

                    insert_matched_article(source_article_id,
                                           target_article_id,
                                           source_sentence,
                                           target_sentence,
                                           source_article_text,
                                           target_article_text,
                                           str(similar_named_entities),
                                           database_cursor)
                    print(source_sentence, target_sentence, similar_named_entities, '\n')
                database_connection.commit()

                # Finder Articles through sentences OK
                # Get Articles Sentences OK
                # Run text named entity analyzer OK
                # Persist results in article_similarity table: OK
                #    source_article_id, source_text, source_language, target_article_id, target_text, target_language, similar named entities OK
                # optional: get articles urls into a table?
                # optional: check articles similarity in external tool?

    finally:
        if database_connection is not None:
            database_connection.close()