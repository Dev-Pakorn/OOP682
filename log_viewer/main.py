from pyside6.QtWidgets import QApplication
from services.mock_source import MockLogSource
from ui.main_window import MainWindow


def main():
    print("Hello from log-viewer!")


if __name__ == "__main__":
    app = QApplication([])
    source = MockLogSource()
    viewer = MainWindow(source)
    viewer.show()
    main()

