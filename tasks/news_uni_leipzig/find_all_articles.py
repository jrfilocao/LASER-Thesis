#!/usr/bin/python3

import argparse
from finding_articles import find_articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finding articles in all languages')
    parser.add_argument('--file-name', required=True,
                        help='news articles file name')
    parser.add_argument('--line-count', type=int, required=True,
                        help='minimum line count of an article')
    parser.add_argument('--average-line-word-count', type=int, required=True,
                        help='minimum average word count of a line in a article')
    args = parser.parse_args()

    find_articles(args.file_name, args.line_count, args.average_line_word_count)
