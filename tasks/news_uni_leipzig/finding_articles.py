#!/usr/bin/python3


def find_articles(file_name, minimum_number_of_consecutive_lines, minimum_average_word_count_of_a_line):
    file_lines = _get_file_lines(file_name)
    articles = _parse_articles(file_lines, minimum_number_of_consecutive_lines, minimum_average_word_count_of_a_line)
    # _write_article_count_to_console(articles)
    return articles


def _get_file_lines(file_name):
    with open(file_name, "r") as input_file:
        file_lines = input_file.readlines()
    return file_lines


def _parse_articles(file_lines, minimum_number_of_consecutive_lines, minimum_average_word_count_of_a_line):
    articles = []
    article = []
    for file_line in file_lines:
        if not file_line.strip():
            article_line_count = len(article)
            if article_line_count >= minimum_number_of_consecutive_lines:
                article_word_count = 0
                for article_line in article:
                    article_line_word_count = len(article_line.split())
                    article_word_count += article_line_word_count
                article_average_line_word_count = article_word_count / article_line_count
                if article_average_line_word_count > minimum_average_word_count_of_a_line:
                    articles.append(article)
            article = []
        else:
            article.append(file_line)
    return articles


def _write_article_count_to_console(articles):
    print("Total articles found", len(articles))