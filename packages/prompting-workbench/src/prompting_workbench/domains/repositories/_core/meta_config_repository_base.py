from abc import abstractmethod

from prompting_workbench.core.repositories.repository_base import (
    RepositoryBase,
)


class MetaConfigRepositoryBase(RepositoryBase):
    def __init__(self, plugin_instance):
        super().__init__()
        self.plugin_instance = plugin_instance

    @abstractmethod
    def get_project_plugin_meta_config(self, config_filename: str) -> dict:
        pass

    @abstractmethod
    def get_prompt_plugin_meta_config(
        self, prompt_id: str, config_filename: str
    ) -> dict:
        pass
