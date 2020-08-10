from reporting.report_writer import write_metric_chart_into_file

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
    for file_line in file_lines:
        if KEY_VALUE_SEPARATOR not in file_line:
            metrics[file_line.strip()] = (thresholds_x, values_y)
            thresholds_x = []
            values_y = []
        else:
            threshold, value = file_line.split(KEY_VALUE_SEPARATOR)
            thresholds_x.append(FLOAT_THREE_DECIMALS % float(threshold))
            values_y.append(FLOAT_TWO_DECIMALS % float(value))
    return metrics


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

    for metric_index in range(metrics_count):
        de_pt_metric_name = de_pt_metric_keys[metric_index]
        en_pt_metric_name = de_pt_metric_name.replace(DE_PT_STRING, EN_PT_STRING).strip()
        en_de_metric_name = de_pt_metric_name.replace(DE_PT_STRING, EN_DE_STRING).strip()

        metric_name = de_pt_metric_name.replace(DE_PT_STRING, EMPTY)

        write_metric_chart_into_file(metric_name,
                                     en_de_metrics[en_de_metric_name],
                                     en_pt_metrics[en_pt_metric_name],
                                     de_pt_metrics[de_pt_metric_name])

