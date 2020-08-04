import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

THRESHOLD_PRECISION_FORMAT = '.3f'


def write_report_entries_into_csv_file(sentence_pair_score_threshold, report_entries, output_report_base_file_name):
    formatted_threshold = format(sentence_pair_score_threshold, THRESHOLD_PRECISION_FORMAT)
    file_name = output_report_base_file_name + '_statistics_{}.txt'.format(formatted_threshold)
    with open(file_name, 'w') as report_file:
        for report_entry in report_entries:
            report_file.write(str(report_entry) + '\n')


def write_article_pair_results_into_file(sentence_pair_score_threshold, result_rows, output_report_base_file_name, language, type):
    formatted_threshold = format(sentence_pair_score_threshold, THRESHOLD_PRECISION_FORMAT)
    file_name = output_report_base_file_name + '_article_pairs_{}_{}_{}.txt'.format(language, formatted_threshold, type)
    with open(file_name, 'w') as report_file:
        for result_row in result_rows:
            report_file.write(str(result_row) + '\n')


def write_statistics_reports_into_file(statistics_reports, output_file_name):
    with open(output_file_name, 'w') as output_file:
        thresholds = list(statistics_reports)  # x
        report_entry_count = len(statistics_reports[thresholds[0]])  # y

        for report_entry_index in range(report_entry_count):
            report_entry_name = statistics_reports[thresholds[0]][report_entry_index][0]
            if 'language' in report_entry_name:
                continue
            for threshold in thresholds:
                output_file.write(threshold)
                output_file.write(';')
                output_file.write(statistics_reports[threshold][report_entry_index][1] + '\n')


def write_consolidate_statistics_diagram_into_file(statistics_reports, output_report_base_file_name):
    base_file_name = output_report_base_file_name + '_diagram_{}'

    thresholds = list(statistics_reports) # x
    report_entry_count = len(statistics_reports[thresholds[0]]) # y

    for report_entry_index in range(report_entry_count):
        report_entry_name = statistics_reports[thresholds[0]][report_entry_index][0]
        if 'language' in report_entry_name:
            continue

        file_name = base_file_name.format(report_entry_name).replace(' ', '_')

        fig = plt.figure()
        fig.tight_layout()
        plt.xlabel('x - thresholds')
        plt.ylabel('y - ' + report_entry_name)
        plt.title(report_entry_name)

        x = []
        y = []

        for threshold in thresholds:
            x.append(threshold)
            y.append(statistics_reports[threshold][report_entry_index][1])

        plt.plot(x, y)
        fig.savefig(file_name, bbox_inches='tight')


def write_charts_for_methods_into_file():
    x1 = [1, 2, 3]

    y1 = [4, 5, 6]

    x2 = [1, 2, 3, 4, 5]

    y2 = [6, 7, 6.5, 3, 4]

    x = np.linspace(0, 10, num=11, endpoint=True)
    y = np.cos(-x**2/9.0)

    fig = plt.figure()
    fig.tight_layout()

    plt.xlim(0, 11)
    plt.ylim(-2, 10)

    plt.xlabel('Thresholds')
    plt.ylabel('Scores' )
    plt.title('Example Chart')

    plt.plot(x1, y1, 'bo--', x, y, 'r+--')

    plt.legend(["Dataset 1", "Dataset 2"])

    file_name = "chart_for_methods"

    fig.savefig(file_name, bbox_inches='tight')


if __name__ == "__main__":
    write_charts_for_methods_into_file()