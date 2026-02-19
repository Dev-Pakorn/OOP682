import csv
from log_viewer.interfaces.data_source import ILogSource

class CSVLogSource(ILogSource):
    def __init__(self, filepath : str):
        self.filepath = filepath

    def get_logs(self):
        log = []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    log.append(' | '.join(row))
        except FileNotFoundError:
            log.append("Error: CSV File not found")
        return log