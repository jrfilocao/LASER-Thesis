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


def write_metric_chart_into_file(metric_name, metric):
    fig = plt.figure()
    fig.tight_layout()

    plt.xlabel('Margin threshold')
    formatted_metric_name = get_metric_name_multiple_languages(metric_name)
    plt.ylabel(formatted_metric_name)
    plt.title('')

    plt.plot(metric[0], metric[1], 'r+--', linewidth=0.7)

    plt.legend(['en-pt'])

    file_name = 'output/' + metric_name

    fig.savefig(file_name, bbox_inches='tight')


def write_chart_with_four_metrics_into_file(metric_name, first_metric, second_metric, third_metric, fourth_metric, language_pair_name):
    fig = plt.figure()
    fig.tight_layout()

    plt.xlabel('Margin threshold')
    plt.ylabel(metric_name)
    plt.title('')

    plt.plot(first_metric[0], first_metric[1], 'b+--', linewidth=0.7, label='ne ≥ 1 and ps ≥ 1')
    plt.plot(first_metric[0], second_metric[1], 'gx--', linewidth=0.7, label='ne ≥ 1 and ps ≥ 2')
    plt.plot(first_metric[0], third_metric[1], 'r.--', linewidth=0.7, label='ne ≥ 0 and ps ≥ 2')
    plt.plot(first_metric[0], fourth_metric[1], 'kp--', linewidth=0.7, label='test')

    plt.legend()

    file_name = 'output/' + metric_name + '_' + language_pair_name

    fig.savefig(file_name, bbox_inches='tight')


def write_metric_chart_with_multiple_languages_into_file(metric_name, en_de_metric, en_pt_metric, de_pt_metric):
    fig = plt.figure()
    fig.tight_layout()

    plt.xlabel('Margin threshold')
    formatted_metric_name = get_metric_name_multiple_languages(metric_name)
    plt.ylabel(formatted_metric_name)
    plt.title('')

    plt.plot(en_de_metric[0], en_de_metric[1], 'r+--', linewidth=0.7)
    plt.plot(en_de_metric[0], en_pt_metric[1], 'bx--', linewidth=0.7)
    plt.plot(en_de_metric[0], de_pt_metric[1], 'g.--', linewidth=0.7)

    plt.legend(['en-de', 'en-pt', 'de-pt'])

    file_name = 'output/' + metric_name

    fig.savefig(file_name, bbox_inches='tight')


def write_chart_with_multiple_metrics_into_file(metric_name, first_metric, second_metric, third_metric, language_pair_name):
    fig = plt.figure()
    fig.tight_layout()

    plt.xlabel('Margin threshold')
    formatted_metric_name = get_metric_name_multiple_metrics(metric_name)
    plt.ylabel(formatted_metric_name)
    plt.title('')

    plt.plot(first_metric[0], first_metric[1], 'b+--', linewidth=0.7, label='ne ≥ 1 and ps ≥ 1')
    plt.plot(first_metric[0], second_metric[1], 'gx--', linewidth=0.7, label='ne ≥ 1 and ps ≥ 2')
    plt.plot(first_metric[0], third_metric[1], 'r.--', linewidth=0.7, label='ne ≥ 0 and ps ≥ 2')

    plt.legend()

    file_name = 'output/' + metric_name + '_' + language_pair_name

    fig.savefig(file_name, bbox_inches='tight')


def write_chart_with_precision_and_recall(matching_metric_names, metrics, language_pair_name):
    fig = plt.figure()
    fig.tight_layout()

    plt.xlabel('Margin threshold')
    plt.ylabel('Precision (%) and Recall (%)')
    plt.title('')

    plt.plot(metrics[matching_metric_names[0]][0], metrics[matching_metric_names[0]][1], marker='+', linestyle='solid', color='red', linewidth=0.7, label='And Precision')
    plt.plot(metrics[matching_metric_names[1]][0], metrics[matching_metric_names[1]][1], marker='+', linestyle='dashed', color='red', linewidth=0.7, label='And Recall')
    plt.plot(metrics[matching_metric_names[2]][0], metrics[matching_metric_names[2]][1], marker='x', linestyle='solid', color='blue', linewidth=0.7, label='Or Precision')
    plt.plot(metrics[matching_metric_names[3]][0], metrics[matching_metric_names[3]][1], marker='x', linestyle='dashed', color='blue', linewidth=0.7, label='Or Recall')
    plt.plot(metrics[matching_metric_names[4]][0], metrics[matching_metric_names[4]][1], marker='.', linestyle='solid', color='green', linewidth=0.7, label='Only Precision')
    plt.plot(metrics[matching_metric_names[5]][0], metrics[matching_metric_names[5]][1], marker='.', linestyle='dashed', color='green', linewidth=0.7, label='And Recall')

    plt.legend()

    file_name = 'output/' + 'precision_vs_recall_' + language_pair_name

    fig.savefig(file_name, bbox_inches='tight')


def get_metric_name_multiple_metrics(metric_name):
    name_without_underline_capitalized = metric_name.replace('_', ' ').capitalize()
    if name_without_underline_capitalized == 'F1':
        name_without_underline_capitalized = name_without_underline_capitalized + ' score'
    if name_without_underline_capitalized in ['Precision', 'F1 score', 'Recall']:
        name_without_underline_capitalized = name_without_underline_capitalized + ' (%)'
    return name_without_underline_capitalized


def get_metric_name_multiple_languages(metric_name):
    name_without_underline_capitalized = metric_name.split('__')[-1].replace('_', ' ').capitalize()
    if name_without_underline_capitalized == 'F1 measure':
        name_without_underline_capitalized = 'F1 score'
    if name_without_underline_capitalized in ['Precision', 'F1 score', 'Recall']:
        name_without_underline_capitalized = name_without_underline_capitalized + ' (%)'
    return name_without_underline_capitalized


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    mean, amp = 40000, 20000
    t = np.arange(50)
    s1 = np.sin(t) * amp + mean  # synthetic ts, but closer to my data

    fig, ax1 = plt.subplots()
    ax1.plot(t, s1, 'b-')

    ax1.set_xlabel('time')
    mn, mx = ax1.set_ylim(mean - amp, mean + amp)
    ax1.set_ylabel('km$^3$/year')

    km3yearToSv = 31.6887646e-6

    ax2 = ax1.twinx()
    ax2.set_ylim(mn * km3yearToSv, mx * km3yearToSv)
    ax2.set_ylabel('Sv')

    plt.show()