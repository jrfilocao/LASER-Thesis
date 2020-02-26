def write_report_entries_into_csv_file(sentence_pair_score_threshold, report_entries):
    file_name = 'output_files/report_{}.txt'.format(sentence_pair_score_threshold)
    with open(file_name, 'w') as report_file:
        for report_entry in report_entries:
            report_file.write(str(report_entry))