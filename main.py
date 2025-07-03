import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = MainWindow(resource_path_fn=resource_path)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()