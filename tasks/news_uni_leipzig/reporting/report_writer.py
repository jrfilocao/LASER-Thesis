def write_report_entries_into_csv_file(sentence_pair_score_threshold, report_entries, output_report_base_file_name):
    file_name = output_report_base_file_name + '_key_value_{}.txt'.format(sentence_pair_score_threshold)
    with open(file_name, 'w') as report_file:
        for report_entry in report_entries:
            report_file.write(str(report_entry))


def write_article_pair_results_into_file(sentence_pair_score_threshold, result_rows, output_report_base_file_name, language, type):
    file_name = output_report_base_file_name + '_pairs_{}_{}_{}.txt'.format(language, sentence_pair_score_threshold, type)
    with open(file_name, 'w') as report_file:
        for result_row in result_rows:
            report_file.write(result_row)