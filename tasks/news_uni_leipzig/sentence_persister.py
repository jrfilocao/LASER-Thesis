#!/usr/bin/python3

import argparse


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Persisting sentences from files in Redis')
    parser.add_argument('--sentence-files', nargs='+', help='sentence files to be processed', required=True)
    return parser


if __name__ == "__main__":

    parser = _get_argument_parser()
    arguments = parser.parse_args()

    for sentence_file in arguments.sentence_files:
        print(sentence_file)