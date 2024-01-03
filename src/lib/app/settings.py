import pydantic
import pydantic_settings

import lib.app.split_settings as app_split_settings


class Settings(pydantic_settings.BaseSettings):
    logger: app_split_settings.LoggingSettings = app_split_settings.LoggingSettings()
    ui: app_split_settings.UISettings = app_split_settings.UISettings()
