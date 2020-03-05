THRESHOLD_PRECISION_FORMAT = '.3f'


def write_report_entries_into_csv_file(sentence_pair_score_threshold, report_entries, output_report_base_file_name):
    formatted_threshold = format(sentence_pair_score_threshold, THRESHOLD_PRECISION_FORMAT)
    file_name = output_report_base_file_name + '_statistics_{}.txt'.format(formatted_threshold)
    with open(file_name, 'w') as report_file:
        for report_entry in report_entries:
            report_file.write(str(report_entry))


def write_article_pair_results_into_file(sentence_pair_score_threshold, result_rows, output_report_base_file_name, language, type):
    formatted_threshold = format(sentence_pair_score_threshold, THRESHOLD_PRECISION_FORMAT)
    file_name = output_report_base_file_name + '_article_pairs_{}_{}_{}.txt'.format(language, formatted_threshold, type)
    with open(file_name, 'w') as report_file:
        for result_row in result_rows:
            report_file.write(str(result_row) + '\n')