import os

from prompting_workbench.core.utils.io import get_json_content
from prompting_workbench.domains.repositories._core.fs_repository_base import (
    FileSystemRepositoryBase,
)
from prompting_workbench.domains.repositories._core.meta_config_repository_base import (
    MetaConfigRepositoryBase,
)


class MetaConfigFileSystemRepository(
    MetaConfigRepositoryBase, FileSystemRepositoryBase
):
    def __init__(self, plugin_instance):
        super().__init__(plugin_instance)

    def get_project_plugin_config_dir(self) -> str:
        if not self.plugin_instance or not self.plugin_instance.project:
            raise ValueError("Plugin instance or project is not set")

        project_dir = self.plugin_instance.project.repository.get_project_dir()

        if not os.path.isdir(project_dir):
            raise ValueError("Project does not exist")

        return os.path.join(
            project_dir, ".config", self.plugin_instance.get_plugin_name()
        )

    def get_prompt_plugin_config_dir(self, prompt_id: str) -> str:
        if not self.plugin_instance or not self.plugin_instance.project:
            raise ValueError("Plugin instance or project is not set")

        project_prompt = self.plugin_instance.project.get_prompt_by_id(prompt_id)

        if not project_prompt:
            raise ValueError(f"Prompt with ID {prompt_id} does not exist in project")

        prompt_config_dir = os.path.join(
            project_prompt.repository.get_prompt_dir(
                self.plugin_instance.project.project_id, prompt_id
            ),
            ".config",
            self.plugin_instance.get_plugin_name(),
        )

        if not os.path.isdir(prompt_config_dir):
            raise ValueError(f"Prompt config directory for {prompt_id} does not exist")

        return prompt_config_dir

    def get_project_plugin_meta_config(self, config_name: str) -> dict:
        try:
            plugin_config_dir = self.get_project_plugin_config_dir()
            config_filename = f"{config_name}.json"
            meta_config_path = os.path.join(plugin_config_dir, config_filename)

            if not os.path.isfile(meta_config_path):
                raise ValueError(
                    f"Meta config for project {config_filename} does not exist"
                )
            return get_json_content(meta_config_path)
        except ValueError:
            return {}

    def get_prompt_plugin_meta_config(self, prompt_id: str, config_name: str) -> dict:
        try:
            prompt_config_dir = self.get_prompt_plugin_config_dir(prompt_id)
            config_filename = f"{config_name}.json"
            meta_config_path = os.path.join(prompt_config_dir, config_filename)

            if not os.path.isfile(meta_config_path):
                raise ValueError(
                    f"Meta config for prompt {prompt_id} and file {config_filename} does not exist"
                )

            return get_json_content(meta_config_path)
        except ValueError:
            return {}
