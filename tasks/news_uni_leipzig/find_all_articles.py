#!/usr/bin/python3

import argparse
import syntok.segmenter as segmenter
from finding_articles import find_articles


def get_argumet_parser():
    parser = argparse.ArgumentParser(description='Finding articles for all languages in crawled news texts')
    parser.add_argument('--input-file-name', required=True,
                        help='input file name of news articles in a specific language')
    parser.add_argument('--line-count', type=int, required=True,
                        help='minimum count of consecutive lines to form an article')
    parser.add_argument('--average-line-word-count', type=int, required=True,
                        help='minimum average word count in a line to form an article')
    return parser


if __name__ == "__main__":
    parser = get_argumet_parser()
    arguments = parser.parse_args()
    articles = find_articles(arguments.file_name, arguments.line_count, arguments.average_line_word_count)

