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

    def set_filter_strategy(self, strategy: IFilterStrategy):
        self.filter_strategy = strategy

    def load_data(self):
        raw_logs = self.source.get_logs()
        
        filtered_logs = self.filter_strategy.filter(raw_logs)
        
        self.list_widget.clear()
        self.list_widget.addItems(filtered_logs)