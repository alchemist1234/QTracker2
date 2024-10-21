from src.settings.default_settings import SettingKey
from src.settings.settings import Settings

if __name__ == '__main__':
    print(SettingKey.main_width)
    print(SettingKey.main_width.value)
    print(list(SettingKey))
