from reporting.report_writer import *

EMPTY = ''
DE_PT_STRING = 'de_pt'
EN_PT_STRING = 'en_pt'
EN_DE_STRING = 'en_de'
KEY_VALUE_SEPARATOR = ';'
FLOAT_TWO_DECIMALS = '%.2f'
FLOAT_THREE_DECIMALS = '%.3f'


def _get_file_lines(file_name):
    with open(file_name, "r") as input_file:
        file_lines = input_file.readlines()
    return file_lines


def get_metrics(file_path):
    file_lines = _get_file_lines(file_path)
    thresholds_x = []
    values_y = []
    metrics = {}
    current_metric_name = ''
    for file_line in file_lines:
        if KEY_VALUE_SEPARATOR not in file_line:
            if not current_metric_name:  # initial iteration
                current_metric_name = file_line.strip()
                continue
            metrics[current_metric_name] = (thresholds_x, values_y)
            current_metric_name = file_line.strip()
            thresholds_x = []
            values_y = []
        else:
            threshold, value = file_line.split(KEY_VALUE_SEPARATOR)
            thresholds_x.append(float(threshold.strip()))
            values_y.append(float(value.strip()))
    metrics[current_metric_name] = (thresholds_x, values_y)
    return metrics


def create_multilingual_diagrams(metrics_count, de_pt_metric_keys, en_de_metrics, en_pt_metrics, de_pt_metrics):
    for metric_index in range(metrics_count):
        de_pt_metric_name = de_pt_metric_keys[metric_index]
        en_pt_metric_name = de_pt_metric_name.replace(DE_PT_STRING, EN_PT_STRING).strip()
        en_de_metric_name = de_pt_metric_name.replace(DE_PT_STRING, EN_DE_STRING).strip()

        metric_name = de_pt_metric_name.replace(DE_PT_STRING, EMPTY)

        write_metric_chart_with_multiple_languages_into_file(metric_name,
                                                             en_de_metrics[en_de_metric_name],
                                                             en_pt_metrics[en_pt_metric_name],
                                                             de_pt_metrics[de_pt_metric_name])


def create_multi_metric_diagrams(metric_name, keys, metrics, language_pair_name):
    matching_metric_names = [metric_element for metric_element in keys if metric_name in metric_element]
    write_chart_with_multiple_metrics_into_file(metric_name,
                                                metrics[matching_metric_names[0]],
                                                metrics[matching_metric_names[1]],
                                                metrics[matching_metric_names[2]],
                                                language_pair_name)


def create_precision_recall_diagrams(keys, metrics, language_pair_name):
    matching_metric_names = [metric_element for metric_element in keys if 'precision' in metric_element or 'recall' in metric_element]
    sorted_matching_metric_names = sorted(matching_metric_names)
    write_chart_with_precision_and_recall(sorted_matching_metric_names,
                                          metrics,
                                          language_pair_name)


if __name__ == "__main__":
    de_pt_file_path = '../input_files/statistic_reports_de_pt.txt'
    en_de_file_path = '../input_files/statistic_reports_en_de.txt'
    en_pt_file_path = '../input_files/statistic_reports_en_pt.txt'

    de_pt_metrics = get_metrics(de_pt_file_path)
    en_de_metrics = get_metrics(en_de_file_path)
    en_pt_metrics = get_metrics(en_pt_file_path)

    metrics_count = len(de_pt_metrics.keys())

    de_pt_metric_keys = list(de_pt_metrics.keys())
    en_de_metric_keys = list(en_de_metrics.keys())
    en_pt_metric_keys = list(en_pt_metrics.keys())

    # create_multilingual_diagrams(metrics_count, de_pt_metric_keys, en_de_metrics, en_pt_metrics, de_pt_metrics)
    #
    # create_multi_metric_diagrams('precision', de_pt_metric_keys, de_pt_metrics, 'de_pt')
    # create_multi_metric_diagrams('f1', de_pt_metric_keys, de_pt_metrics, 'de_pt')
    # create_multi_metric_diagrams('recall', de_pt_metric_keys, de_pt_metrics, 'de_pt')
    # create_multi_metric_diagrams('average_matched_sentence_count', de_pt_metric_keys, de_pt_metrics, 'de_pt')
    #
    # create_multi_metric_diagrams('precision', en_pt_metric_keys, en_pt_metrics, 'en_pt')
    # create_multi_metric_diagrams('f1', en_pt_metric_keys, en_pt_metrics, 'en_pt')
    # create_multi_metric_diagrams('recall', en_pt_metric_keys, en_pt_metrics, 'en_pt')
    # create_multi_metric_diagrams('average_matched_sentence_count', en_pt_metric_keys, en_pt_metrics, 'en_pt')
    #
    # create_multi_metric_diagrams('precision', en_de_metric_keys, en_de_metrics, 'en_de')
    # create_multi_metric_diagrams('f1', en_de_metric_keys, en_de_metrics, 'en_de')
    # create_multi_metric_diagrams('recall', en_de_metric_keys, en_de_metrics, 'en_de')
    # create_multi_metric_diagrams('average_matched_sentence_count', en_de_metric_keys, en_de_metrics, 'en_de')

    create_precision_recall_diagrams(en_de_metric_keys, en_de_metrics, 'en_de')
    create_precision_recall_diagrams(en_pt_metric_keys, en_pt_metrics, 'en_pt')
    create_precision_recall_diagrams(de_pt_metric_keys, de_pt_metrics, 'de_pt')
