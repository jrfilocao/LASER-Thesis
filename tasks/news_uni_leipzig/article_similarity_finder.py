#!/usr/bin/python3


import argparse
import psycopg2


def _get_database_connection():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Analysing article similarity through similar sentences')
    parser.add_argument('--sentence-candidate-file-paths', nargs='+', help='sentence candidate files to be analysed', required=True)
    return parser


def get_score_sentences_triple():
    score_sentences = sentence_candidate.split('\t')
    if len(score_sentences) == 3:
        for score_sentences_element in score_sentences:
            if not score_sentences_element.strip():
                raise ValueError
        return score_sentences[0].strip(), score_sentences[1].strip(), score_sentences[2].strip()
    raise ValueError


if __name__ == "__main__":
    parser = _get_argument_parser()
    arguments = parser.parse_args()

    # TODO add id_sentence_pair_persister
    try:
        database_connection = _get_database_connection()
        database_cursor = database_connection.cursor()

        for sentence_candidate_file_path in arguments.sentence_candidate_file_paths:
            with open(sentence_candidate_file_path, 'r') as  sentence_candidate_file:
                sentence_candidates = sentence_candidate_file.readlines()
                for sentence_candidate in sentence_candidates:
                    try:
                        score, source_sentence, target_sentence = get_score_sentences_triple()
                        print(score, source_sentence, target_sentence)
                    except ValueError:
                        pass

    finally:
        if database_connection is not None:
            database_connection.close()