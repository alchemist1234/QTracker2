from typing import Any
from collections.abc import Iterable

from PySide6.QtCore import QSettings

from src.settings.default_settings import SettingKey, SettingItem


class Settings(object):
    """
    配置类
    """

    def __init__(self, setting_path: str):
        self.setting_path = setting_path
        self.settings = QSettings(setting_path, QSettings.Format.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.init_value()

    def init_value(self) -> None:
        """
        为一些不需要存入文件的值设置初始值
        """
        for key in list(SettingKey):
            item: SettingItem = key.value
            if not item.save_to_file:
                self.set_value(key, item.default_value)

    def int_value(self, key: SettingKey) -> int:
        """
        获取配置值 (int类型)
        :param key: 配置项
        :return: int类型配置值
        """
        return int(self.value(key))

    def float_value(self, key: SettingKey) -> float:
        """
        获取配置值 (float类型)
        :param key: 配置项
        :return: float类型配置值
        """
        return float(self.value(key))

    def boolean_value(self, key: SettingKey) -> bool:
        """
        获取配置值 (bool类型)
        :param key: 配置项
        :return: bool类型配置值
        """
        value = self.value(key)
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def list_value(self, key: SettingKey) -> list:
        """
        获取配置值 (list类型)
        :param key: 配置项
        :return: list类型配置值
        """
        value = self.value(key)
        # 如果是字符串，不把字符开成list
        if isinstance(value, str):
            return [value]
        # 其他可迭代对象，转成list
        return list(value) if isinstance(value, Iterable) else [value]

    def str_value(self, key: SettingKey) -> str:
        """
        获取配置值 (str类型)
        :param key: 配置项
        :return: str类型配置值
        """
        return str(self.value(key))

    def value(self, key: SettingKey) -> Any:
        """
        获取配置值
        :param key: 配置项
        :return: 类型配置值
        """
        item: SettingItem = key.value
        return self.settings.value(f'{item.section}/{item.key}', item.default_value)

    def set_value(self, key: SettingKey, value: Any) -> None:
        """
        设置配置值
        :param key: 配置项
        :param value: 配置值
        """
        item = key.value
        self.settings.setValue(f'{item.section}/{item.key}', value)

    def sync(self) -> None:
        """
        刷新配置到磁盘
        """
        self.settings.sync()
