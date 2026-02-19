import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PySide6.QtWidgets import QApplication
from interfaces.data_source import ILogSource
from services.file_source import FileLogSource
from services.mock_source import MockLogSource
from services.csv_source import CsvLogSource
from ui.main_window import MainWindow

class SourceFactory:
    @staticmethod
    def create_source(source_type: str) -> ILogSource:
        if source_type == "file":
            return FileLogSource("app.log")
        elif source_type == "mock":
            return MockLogSource()
        elif source_type == "csv":
            return CsvLogSource("data.csv")
        else:
            raise ValueError(f"Unknown type: {source_type}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        selected_type = "csv"
        source = SourceFactory.create_source(selected_type) 
        viewer = MainWindow(source)
        viewer.setWindowTitle(f"Log Viewer - Source: {selected_type.upper()}")
        
        viewer.load_data()
        viewer.show()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการรันโปรแกรม: {e}")