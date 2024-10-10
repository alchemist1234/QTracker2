from PySide6.QtCore import QSettings

from src.settings.default_settings import *


class Settings(object):
    def __init__(self, setting_path: str):
        self.setting_path = setting_path
        self.settings = QSettings(setting_path, QSettings.Format.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.set_value(index_filter, [])

    def int_value(self, item: SettingItem):
        return int(self.value(item))

    def float_value(self, item: SettingItem):
        return float(self.value(item))

    def boolean_value(self, item: SettingItem):
        value = self.value(item)
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def list_value(self, item: SettingItem):
        value = self.value(item)
        return value if isinstance(value, list) else [value]

    def str_value(self, item: SettingItem):
        return str(self.value(item))

    def value(self, item: SettingItem):
        return self.settings.value(f'{item.section}/{item.key}', item.default_value)

    def set_value(self, item: SettingItem, value: Any):
        self.settings.setValue(f'{item.section}/{item.key}', value)

    def sync(self):
        self.settings.sync()
