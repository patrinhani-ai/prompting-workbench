from pydantic_settings import BaseSettings, SettingsConfigDict


class PromptWorkbenchSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PMPT_WRKBNCH_",
        env_file=".env.wrkbnch",
        yaml_file=".wrkbnch.yaml",
        env_file_encoding="utf-8",
    )

    projects_dir: str = "./wrkbnch_space"


settings = PromptWorkbenchSettings()
