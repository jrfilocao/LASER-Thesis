def write_report_entries_into_csv_file(report_entries):
    with open('output_files/report.txt', 'w') as report_file:
        for report_entry in report_entries:
            report_file.write(str(report_entry))