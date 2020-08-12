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
            output_file.write(report_entry_name + '\n')
            for threshold in thresholds:
                output_file.write(str(threshold))
                output_file.write(';')
                output_file.write(str(statistics_reports[threshold][report_entry_index][1]) + '\n')


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


def write_metric_chart_into_file(metric_name, en_de_metric, en_pt_metric, de_pt_metric):
    # x1 = [1, 2, 3]
    #
    # y1 = [4, 5, 6]
    #
    # x2 = np.linspace(0, 10, num=11, endpoint=True)
    # y2 = np.cos(-x2**2/9.0)

    fig = plt.figure()
    fig.tight_layout()

    # plt.xlim(0, 1.5)
    # plt.ylim(0, 100)

    plt.xlabel('Thresholds')
    plt.ylabel('Scores')
    plt.title(metric_name)

    plt.plot(en_de_metric[0], en_de_metric[1], 'bo--')
    plt.plot(en_de_metric[0], en_pt_metric[1], 'r+--')
    plt.plot(en_de_metric[0], de_pt_metric[1], 'yo--')

    plt.legend(['English-German', 'English-Portuguese', 'German-Portuguese'])

    file_name = 'output/' + metric_name

    fig.savefig(file_name, bbox_inches='tight')


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    t = np.arange(1000) / 100.
    x = np.sin(2 * np.pi * 10 * t)
    y = np.cos(2 * np.pi * 10 * t)

    fig = plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)

    ax1.plot(t, x)
    ax2.plot(t, y)

    ax1.get_shared_x_axes().join(ax1, ax2)
    ax1.set_xticklabels([])
    # ax2.autoscale() ## call autoscale if needed

    plt.show()