import pathlib

import pydantic_settings

import lib.app.split_settings.utils as app_split_settings_utils


class UISettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=app_split_settings_utils.ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="UI_",
    )

    labs_count: int = 1
    third_lab_schemas_path: pathlib.Path = app_split_settings_utils.BASE_PATH / "lib/ui/design/third"
    variants_count: int = 21
