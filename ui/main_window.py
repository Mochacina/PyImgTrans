import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QProgressDialog, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QThreadPool
from .sidebar import Sidebar
from .drop_zone import DropZone
from .preview import Preview
from core.worker import Worker
from core.converter import ImageConverter
from core.settings import AppSettings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = AppSettings()
        self.threadpool = QThreadPool()
        self.setWindowTitle("Image Converter")

        self.restore_geometry()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        self.sidebar = Sidebar()
        main_area = QWidget()
        main_area_layout = QVBoxLayout(main_area)

        self.drop_zone = DropZone()
        self.preview = Preview()
        
        main_area_splitter = QSplitter(Qt.Orientation.Vertical)
        main_area_splitter.addWidget(self.drop_zone)
        main_area_splitter.addWidget(self.preview)
        main_area_splitter.setSizes([400, 400])
        
        main_area_layout.addWidget(main_area_splitter)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(main_area)
        self.main_splitter = splitter # To save/restore state

        self.restore_splitter_state()

        # 시그널 연결
        self.drop_zone.filesDropped.connect(self.sidebar.add_dropped_files)
        self.sidebar.convert_button.clicked.connect(self.start_conversion)
        self.sidebar.file_list.currentItemChanged.connect(self.update_preview)
        self.sidebar.previewCleared.connect(self.clear_preview)

        self.load_styles()

    def update_preview(self, current, previous):
        if current:
            self.preview.set_preview_image(current.text())
        # If the list becomes empty, current is None
        elif self.sidebar.file_list.count() == 0:
            self.clear_preview()

    def clear_preview(self):
        self.preview.set_preview_image(None)

    def start_conversion(self):
        files = [self.sidebar.file_list.item(i).text() for i in range(self.sidebar.file_list.count())]
        if not files:
            QMessageBox.warning(self, "No Files", "Please add files to convert.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not output_dir:
            return

        self.progress_dialog = QProgressDialog("Converting files...", "Cancel", 0, len(files), self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)
        self.completed_tasks = 0

        for i, file_path in enumerate(files):
            worker = Worker(self.convert_image, file_path, output_dir)
            worker.signals.finished.connect(self.conversion_finished)
            worker.signals.error.connect(self.conversion_error)
            self.threadpool.start(worker)

    def convert_image(self, file_path, output_dir, progress_callback):
        try:
            output_format = self.sidebar.format_combo.currentText()
            filename = os.path.basename(file_path)
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{name}.{output_format.lower()}")

            converter = ImageConverter(file_path, output_path)

            if self.sidebar.resize_check.isChecked():
                width = self.sidebar.width_spin.value()
                height = self.sidebar.height_spin.value()
                keep_aspect = self.sidebar.aspect_check.isChecked()
                converter.resize(width, height, keep_aspect)

            converter.convert(output_format, self.sidebar.quality_slider.value())
        except Exception as e:
            print(f"Error converting {file_path}: {e}")


    def conversion_finished(self):
        self.completed_tasks += 1
        self.progress_dialog.setValue(self.completed_tasks)
        if self.completed_tasks == self.sidebar.file_list.count():
            QMessageBox.information(self, "Success", "All files converted successfully.")

    def conversion_error(self, err):
        print("Conversion Error:", err)
        QMessageBox.critical(self, "Error", f"An error occurred during conversion:\n{err}")

    def restore_geometry(self):
        geometry = self.settings.load_geometry()
        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.setGeometry(100, 100, 1200, 800)

    def restore_splitter_state(self):
        state = self.settings.load_splitter_state()
        if state:
            self.main_splitter.restoreState(state)
        else:
            self.main_splitter.setSizes([300, 900])

    def closeEvent(self, event):
        self.settings.save_geometry(self.saveGeometry())
        self.settings.save_splitter_state(self.main_splitter.saveState())
        self.sidebar.save_settings()
        event.accept()

    def load_styles(self):
        try:
            with open("resources/styles/dark.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Stylesheet not found.")