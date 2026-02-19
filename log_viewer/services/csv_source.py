import csv
from interfaces.data_source import ILogSource

class CsvLogSource(ILogSource):
    def __init__(self, file_path : str):
        self.filepath = file_path

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