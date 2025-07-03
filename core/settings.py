from PyQt6.QtCore import QSettings

class AppSettings:
    def __init__(self):
        self.settings = QSettings("MyCompany", "PyImgTrans")

    def save_setting(self, key, value):
        self.settings.setValue(key, value)

    def load_setting(self, key, default=None):
        return self.settings.value(key, default)

    def save_geometry(self, geometry):
        self.save_setting("geometry", geometry)

    def load_geometry(self):
        return self.load_setting("geometry")

    def save_splitter_state(self, state):
        self.save_setting("splitter_state", state)

    def load_splitter_state(self):
        return self.load_setting("splitter_state")
        
    def save_conversion_options(self, options):
        self.settings.beginGroup("Conversion")
        for key, value in options.items():
            self.settings.setValue(key, value)
        self.settings.endGroup()

    def load_conversion_options(self):
        options = {}
        self.settings.beginGroup("Conversion")
        for key in self.settings.childKeys():
            options[key] = self.settings.value(key)
        self.settings.endGroup()
        return options