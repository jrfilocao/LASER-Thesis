#!/usr/bin/python3


import argparse
from database_connector import get_database_connection
from sentence_repository import get_articles_from_sentence, get_sentences_from_article
from text_named_entity_analyzer import get_similar_entities_in_crosslingual_texts
from matched_article_repository import insert_matched_article, update_number_of_similar_sentences_in_matched_articles

GOOGLE_DOMAIN = 'com'

MINIMUM_CANDIDATE_SENTENCE_LENGTH = 5


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Analysing article similarity through similar sentences')
    parser.add_argument('--sentence-candidate-file-paths', nargs='+', help='sentence candidate files to be analysed', required=True)
    parser.add_argument('--file-language-pairs', nargs='+', help='language of sentence candidates', required=True)
    return parser


def _get_score_sentences_triple(sentence_candidate):
    score_sentences = sentence_candidate.split('\t')
    if len(score_sentences) == 3:
        for score_sentences_element in score_sentences:
            stripped_score_sentences_element = score_sentences_element.strip()
            if not stripped_score_sentences_element or len(stripped_score_sentences_element) < MINIMUM_CANDIDATE_SENTENCE_LENGTH:
                raise ValueError
        return score_sentences[0].strip(), score_sentences[1].strip(), score_sentences[2].strip()
    raise ValueError


def _get_article_sentences_as_text(sentences):
    return " ".join(sentence_tuple[0] for sentence_tuple in sentences)


def _get_source_target_languages(file_language_pair):
    source_language, target_language = file_language_pair.split('_')
    return source_language, target_language


def _get_named_entity_set_text(named_entity_set):
    if len(named_entity_set) > 0:
        return str(named_entity_set)
    return None


def _update_article_pair_similar_sentences_count(source_article_id, target_article_id, article_similar_sentences_counter):
    article_id_pair = (source_article_id, target_article_id)
    if article_id_pair in article_similar_sentences_counter:
        article_similar_sentences_counter[(source_article_id, target_article_id)] += 1
    else:
        article_similar_sentences_counter[(source_article_id, target_article_id)] = 1


if __name__ == "__main__":
    parser = _get_argument_parser()
    arguments = parser.parse_args()

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        for sentence_candidate_file_path, file_language_pair in zip(arguments.sentence_candidate_file_paths, arguments.file_language_pairs):
            with open(sentence_candidate_file_path, 'r') as sentence_candidate_file:
                sentence_candidate_pairs = sentence_candidate_file.readlines()
                article_pair_similar_sentences_counter = {}
                for sentence_candidate_pair in sentence_candidate_pairs:
                    try:
                        score, source_sentence, target_sentence = _get_score_sentences_triple(sentence_candidate_pair)
                        source_article_id = get_articles_from_sentence(source_sentence, database_cursor)
                        target_article_id = get_articles_from_sentence(target_sentence, database_cursor)

                        if source_article_id is None or target_article_id is None:
                            print(source_article_id, target_article_id, ' => None')
                            continue

                        source_article_sentences = get_sentences_from_article(source_article_id, database_cursor)
                        target_article_sentences = get_sentences_from_article(target_article_id, database_cursor)

                        source_article_text = _get_article_sentences_as_text(source_article_sentences)
                        target_article_text = _get_article_sentences_as_text(target_article_sentences)

                        source_language, target_language = _get_source_target_languages(file_language_pair)

                        similar_named_entities = get_similar_entities_in_crosslingual_texts(source_article_text,
                                                                                            source_language,
                                                                                            target_article_text,
                                                                                            target_language)

                        similar_named_entities_text = _get_named_entity_set_text(similar_named_entities)

                        insert_matched_article(source_article_id,
                                               target_article_id,
                                               source_sentence,
                                               target_sentence,
                                               source_article_text,
                                               target_article_text,
                                               source_language,
                                               target_language,
                                               None,
                                               None,
                                               similar_named_entities_text,
                                               database_cursor)
                        _update_article_pair_similar_sentences_count(source_article_id, target_article_id, article_pair_similar_sentences_counter)
                    except Exception as e:
                        print('Error processing sentence candidate pair', sentence_candidate_pair, e)
                        continue
                update_number_of_similar_sentences_in_matched_articles(article_pair_similar_sentences_counter, database_cursor)
    finally:
        if database_connection is not None:
            database_connection.close()