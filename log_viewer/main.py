from PySide6.QtWidgets import QApplication
from log_viewer.interfaces.data_source import ILogSource
from log_viewer.services.file_source import FileLogSource
from log_viewer.services.mock_source import MockLogSource
from log_viewer.ui.main_window import MainWindow
from log_viewer.services.csv_source import CSVLogSource

class SourceFactory:
    @staticmethod
    def create_source(source_type: str) -> ILogSource:
        if source_type == "file":
            return FileLogSource("app.log")
        elif source_type == "mock":
            return MockLogSource()
        elif source_type == "csv":
            return CSVLogSource("logs.csv")
        else:
            raise ValueError(f"Unknown type: {source_type}")

if __name__ == "__main__":
    app = QApplication([])
    source = SourceFactory.create_source("csv") 
    
    viewer = MainWindow(source)
    viewer.load_data()
    viewer.show()
    app.exec() 