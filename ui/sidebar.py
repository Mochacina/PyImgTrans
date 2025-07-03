from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout,
                             QFileDialog, QGroupBox, QFormLayout, QComboBox, QSlider,
                             QSpinBox, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from core.settings import AppSettings

class Sidebar(QWidget):
    # Signal to notify when the preview should be cleared
    previewCleared = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings = AppSettings()
        self.setStyleSheet("background-color: #333333;")
        self.setMinimumWidth(250)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 파일 목록
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Files")
        self.remove_button = QPushButton("Remove")
        self.clear_button = QPushButton("Clear All")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        # 설정 패널
        self.settings_group = QGroupBox("Conversion Settings")
        settings_layout = QFormLayout(self.settings_group)

        # 출력 형식
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JPEG", "PNG", "WEBP", "BMP", "TIFF"])
        settings_layout.addRow("Output Format:", self.format_combo)

        # 품질 설정
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(95)
        self.quality_label = QSpinBox()
        self.quality_label.setRange(1, 100)
        self.quality_label.setValue(95)
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_label)
        settings_layout.addRow("Quality:", quality_layout)
        self.quality_slider.valueChanged.connect(self.quality_label.setValue)
        self.quality_label.valueChanged.connect(self.quality_slider.setValue)

        # 크기 조정
        self.resize_check = QCheckBox("Resize Image")
        settings_layout.addRow(self.resize_check)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.aspect_check = QCheckBox("Keep Aspect Ratio")
        self.aspect_check.setChecked(True)
        settings_layout.addRow("Width:", self.width_spin)
        settings_layout.addRow("Height:", self.height_spin)
        settings_layout.addRow(self.aspect_check)
        
        # 변환 버튼
        self.convert_button = QPushButton("Convert")
        
        layout.addWidget(self.settings_group)
        layout.addWidget(self.convert_button)


        # 시그널 연결
        self.add_button.clicked.connect(self.add_files)
        self.remove_button.clicked.connect(self.remove_selected_file)
        self.clear_button.clicked.connect(self.clear_all_files)

        self.load_settings()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.ico)"
        )
        if files:
            self.file_list.addItems(files)

    def remove_selected_file(self):
        list_widget = self.file_list
        selected_items = list_widget.selectedItems()
        if not selected_items:
            return

        current_item = list_widget.currentItem()
        
        for item in selected_items:
            # Check if the removed item is the one being previewed
            if item == current_item:
                self.previewCleared.emit()
            list_widget.takeItem(list_widget.row(item))

    def clear_all_files(self):
        self.file_list.clear()
        self.previewCleared.emit()

    def add_dropped_files(self, files):
        # 유효한 이미지 파일만 필터링
        valid_extensions = ['.png', '.xpm', '.jpg', '.jpeg', '.bmp', '.gif', '.webp', '.tiff', '.ico']
        image_files = [f for f in files if any(f.lower().endswith(ext) for ext in valid_extensions)]
        if image_files:
            self.file_list.addItems(image_files)

    def save_settings(self):
        options = {
            "format": self.format_combo.currentText(),
            "quality": self.quality_slider.value(),
            "resize": self.resize_check.isChecked(),
            "width": self.width_spin.value(),
            "height": self.height_spin.value(),
            "aspect_ratio": self.aspect_check.isChecked()
        }
        self.settings.save_conversion_options(options)

    def load_settings(self):
        options = self.settings.load_conversion_options()
        if not options:
            return
            
        self.format_combo.setCurrentText(options.get("format", "PNG"))
        self.quality_slider.setValue(int(options.get("quality", 95)))
        self.resize_check.setChecked(options.get("resize", "false").lower() == 'true')
        self.width_spin.setValue(int(options.get("width", 1024)))
        self.height_spin.setValue(int(options.get("height", 1024)))
        self.aspect_check.setChecked(options.get("aspect_ratio", "true").lower() == 'true')