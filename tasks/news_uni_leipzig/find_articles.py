#!/bin/python3

ARTICLE_MINIMUM_LINE_COUNT = 5
ARTICLE_MINIMUM_AVERAGE_LINE_WORD_COUNT = 15

with open("wdt_2019-07-08_deu.source", "r") as input_file:
    file_lines = input_file.readlines()

articles = []
article = []
for file_line in file_lines:
    if not file_line.strip():
        print("empty string")
        article_line_count = len(article)
        if article_line_count >= ARTICLE_MINIMUM_LINE_COUNT:
            article_word_count = 0
            for article_line in article:
                article_line_word_count = len(article_line.split())
                article_word_count += article_line_word_count
            article_average_line_word_count = article_word_count / article_line_count
            if article_average_line_word_count > ARTICLE_MINIMUM_AVERAGE_LINE_WORD_COUNT:
                print(article)
                articles.append(article)
            print(article_average_line_word_count)
        article = []
    else:
        article.append(file_line)
        print(len(file_line.split()))