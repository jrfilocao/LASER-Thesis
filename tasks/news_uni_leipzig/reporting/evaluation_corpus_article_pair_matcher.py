import os
import sys
assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'
NEWS_TASK = os.environ['NEWS_TASK']
sys.path.append(NEWS_TASK + '/common')
sys.path.append(NEWS_TASK + '/reporting')


def get_article_pairs_match_count_and_incorrect_pairs_and_average_sentence_count(rows):
    total_matched_sentence_count_in_correct_pairs = 0
    incorrect_article_pairs = []
    correct_article_pairs = set()

    for row in rows:
        if row[0][3:] == row[1][3:]:
            correct_article_pair = (row[0][3:], row[1][3:])
            if correct_article_pair not in correct_article_pairs:
                correct_article_pairs.add(correct_article_pair)
            else:
                print('duplicate', correct_article_pair, row)

            total_matched_sentence_count_in_correct_pairs += row[2]
        else:
            incorrect_article_pairs.append(row)

    correct_article_pairs_count = len(correct_article_pairs)
    average_matched_sentence_count_in_correct_pairs = total_matched_sentence_count_in_correct_pairs / correct_article_pairs_count

    return correct_article_pairs_count, incorrect_article_pairs, average_matched_sentence_count_in_correct_pairs
