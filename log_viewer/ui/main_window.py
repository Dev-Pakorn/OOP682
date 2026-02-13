from PySide6.QtWidgets import *

class MainWindow(QMainWindow):
    # รับ Abstraction เข้ามา (DIP)
    def __init__(self, source: ILogSource):
        super().__init__()
        self.source = source  # Composition
        self.init_ui()

    def load_data(self):
        # UI ไม่รู้ว่าข้อมูลมาจากไหน รู้แค่ get_logs()
        logs = self.source.get_logs()
        self.list_widget.addItems(logs)