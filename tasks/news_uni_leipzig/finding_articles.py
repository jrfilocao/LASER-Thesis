#!/usr/bin/python3


def find_articles(file_name, article_minimum_line_count, article_minimum_average_line_word_count):
    file_lines = _get_file_lines(file_name)
    articles = _parse_articles(file_lines, article_minimum_line_count, article_minimum_average_line_word_count)
    _write_article_count_to_console(articles)


def _get_file_lines(file_name):
    with open(file_name, "r") as input_file:
        file_lines = input_file.readlines()
    return file_lines


def _parse_articles(file_lines, article_minimum_line_count, article_minimum_average_line_word_count):
    articles = []
    article = []
    for file_line in file_lines:
        _get_articles_with_minimum_line_and_word_count(article, articles, file_line, article_minimum_line_count,
                                                       article_minimum_average_line_word_count)
    return articles


def _get_articles_with_minimum_line_and_word_count(article, articles, file_line, article_minimum_line_count,
                                                   article_minimum_average_line_word_count):
    if not file_line.strip():
        article_line_count = len(article)
        if article_line_count >= article_minimum_line_count:
            article_word_count = 0
            for article_line in article:
                article_line_word_count = len(article_line.split())
                article_word_count += article_line_word_count
            article_average_line_word_count = article_word_count / article_line_count
            if article_average_line_word_count > article_minimum_average_line_word_count:
                print("\n")
                print(article)
                articles.append(article)
                print(article_average_line_word_count)
        article.clear()
    else:
        article.append(file_line)


def _write_article_count_to_console(articles):
    print("Total articles found", len(articles))
