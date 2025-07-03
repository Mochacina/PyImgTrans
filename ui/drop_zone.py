from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

class DropZone(QWidget):
    filesDropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Drag & Drop Files Here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #555555;
                padding: 20px;
                font-size: 16px;
            }
        """)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label.setStyleSheet("border: 2px dashed #007acc;")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.label.setStyleSheet("border: 2px dashed #555555;")

    def dropEvent(self, event):
        self.label.setStyleSheet("border: 2px dashed #555555;")
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.filesDropped.emit(files)