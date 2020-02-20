from database_connector import get_database_connection
from report_repository import get_total_sentence_pairs_count


class ReportEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return self.key + ' ' + self.value

    def __str__(self):
        return self.key + ' ' + self.value


def create_report(database_cursor):
    total_sentence_pairs_count = get_total_sentence_pairs_count(database_cursor)
    return ReportEntry('total sentence pairs', str(total_sentence_pairs_count))


if __name__ == "__main__":

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        print(create_report(database_cursor))
    finally:
        if database_connection is not None:
            database_connection.close()
