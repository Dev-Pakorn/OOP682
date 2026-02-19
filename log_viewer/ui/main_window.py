from typing import List
from PySide6.QtWidgets import *
from abc import ABC, abstractmethod

class IFilterStrategy(ABC):
    @abstractmethod
    def filter(self, logs: List[str]) -> List[str]:
        pass

class ErrorOnlyFilter(IFilterStrategy):
    def filter(self, logs: List[str]) -> List[str]:
        return [l for l in logs if "ERROR" in l]

class NoFilter(IFilterStrategy):
    def filter(self, logs: List[str]) -> List[str]:
        return logs

class MainWindow(QMainWindow):
    def __init__(self, source): 
        super().__init__()
        self.source = source
        self.filter_strategy = NoFilter() 
        self.init_ui() 

    def init_ui(self):
        self.setWindowTitle("Log Viewer")
        self.resize(600, 400)
        
        # ส่วนประกอบ UI
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        
        btn_layout = QHBoxLayout()
        self.btn_no_filter = QPushButton("Show All")
        self.btn_error_only = QPushButton("Errors Only")
        
        self.btn_no_filter.clicked.connect(lambda: self.apply_filter(NoFilter()))
        self.btn_error_only.clicked.connect(lambda: self.apply_filter(ErrorOnlyFilter()))
        
        btn_layout.addWidget(self.btn_no_filter)
        btn_layout.addWidget(self.btn_error_only)
        
        layout.addLayout(btn_layout)
        layout.addWidget(self.list_widget)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def apply_filter(self, strategy: IFilterStrategy):
        self.set_filter_strategy(strategy)
        self.load_data() 

    def set_filter_strategy(self, strategy: IFilterStrategy):
        self.filter_strategy = strategy

    def load_data(self):
        raw_logs = self.source.get_logs()
        filtered_logs = self.filter_strategy.filter(raw_logs)
        self.list_widget.clear()
        self.list_widget.addItems(filtered_logs)