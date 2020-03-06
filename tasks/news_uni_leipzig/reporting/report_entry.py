class ReportEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return self.key + ',' + self.value + '\n'

    def __str__(self):
        return self.key + ',' + self.value + '\n'