from collections.abc import Iterable

from PySide6.QtCore import QSettings

from src.settings.default_settings import *


class Settings(object):
    """
    配置类
    """

    def __init__(self, setting_path: str):
        self.setting_path = setting_path
        self.settings = QSettings(setting_path, QSettings.Format.IniFormat)
        self.settings.setFallbacksEnabled(False)
        self.set_value(index_filter, [])
        self.set_value(show_particle, True)
        self.set_value(show_mark, True)
        self.set_value(show_particle, True)

    def init_value(self):
        # TODO 可通过SettingItem的save_to_file字段进行参数初始化，但需要考虑用什么方式实现，目前先把需要重置的参数写死
        pass

    def int_value(self, item: SettingItem) -> int:
        """
        获取配置值 (int类型)
        :param item: 配置项
        :return: int类型配置值
        """
        return int(self.value(item))

    def float_value(self, item: SettingItem) -> float:
        """
        获取配置值 (float类型)
        :param item: 配置项
        :return: float类型配置值
        """
        return float(self.value(item))

    def boolean_value(self, item: SettingItem) -> bool:
        """
        获取配置值 (bool类型)
        :param item: 配置项
        :return: bool类型配置值
        """
        value = self.value(item)
        return value.lower() == 'true' if isinstance(value, str) else bool(value)

    def list_value(self, item: SettingItem) -> list:
        """
        获取配置值 (list类型)
        :param item: 配置项
        :return: list类型配置值
        """
        value = self.value(item)
        # 如果是字符串，不把字符开成list
        if isinstance(value, str):
            return [value]
        # 其他可迭代对象，转成list
        return list(value) if isinstance(value, Iterable) else [value]

    def str_value(self, item: SettingItem) -> str:
        """
        获取配置值 (str类型)
        :param item: 配置项
        :return: str类型配置值
        """
        return str(self.value(item))

    def value(self, item: SettingItem) -> Any:
        """
        获取配置值
        :param item: 配置项
        :return: 类型配置值
        """
        return self.settings.value(f'{item.section}/{item.key}', item.default_value)

    def set_value(self, item: SettingItem, value: Any) -> None:
        """
        设置配置值
        :param item: 配置项
        :param value: 配置值
        """
        self.settings.setValue(f'{item.section}/{item.key}', value)

    def sync(self) -> None:
        """
        刷新配置到磁盘
        """
        self.settings.sync()
