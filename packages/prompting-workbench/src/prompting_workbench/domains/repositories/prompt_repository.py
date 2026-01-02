import os

from prompting_workbench.core.utils.io import get_json_content
from prompting_workbench.domains.models.prompt import PromptModel
from prompting_workbench.domains.repositories._core.fs_repository_base import (
    FileSystemRepositoryBase,
)


class PromptRepository(FileSystemRepositoryBase):
    def get_project_dir(self, project_id: str) -> str:
        if (not project_id) or (project_id.strip() == ""):
            return os.path.join(self.projects_dir)

        return os.path.join(self.projects_dir, project_id)

    def get_prompt_dir(self, project_id: str, prompt_id: str) -> str:
        return os.path.join(self.get_project_dir(project_id), "prompts", prompt_id)

    def get_prompt_config(self, project_id: str, prompt_id: str) -> dict:
        prompt_dir = self.get_prompt_dir(project_id, prompt_id)
        prompt_config_dir_path = os.path.join(prompt_dir, ".config")
        prompt_config_path = os.path.join(prompt_config_dir_path, "meta_info.json")

        if not os.path.isfile(prompt_config_path):
            raise ValueError(
                f"Prompt config for prompt {prompt_id} does not exist in project {project_id}"
            )

        return get_json_content(prompt_config_path)

    def __init__(self):
        super().__init__()

    def get_all_prompt_ids(self, project_id) -> list[str]:
        project_path = self.get_project_dir(project_id)

        if not os.path.isdir(project_path):
            raise ValueError(f"Project {project_id} does not exist")

        prompts_dir_path = os.path.join(project_path, "prompts")

        prompt_ids = []
        for prompt_id in os.listdir(prompts_dir_path):
            if os.path.isdir(os.path.join(prompts_dir_path, prompt_id)):
                prompt_ids.append(prompt_id)

        return sorted(prompt_ids)

    def get_all_prompts(self, project_id) -> list[PromptModel]:
        prompts = []
        for prompt_id in self.get_all_prompt_ids(project_id):
            cur_prompt = self.get_prompt(project_id, prompt_id)
            prompts.append(cur_prompt)

        return prompts

    def get_prompt(self, project_id, prompt_id, defaults: dict = {}) -> PromptModel:
        project_path = self.get_project_dir(project_id)

        if not os.path.isdir(project_path):
            raise ValueError(f"Project {project_id} does not exist")

        prompts_dir_path = os.path.join(project_path, "prompts")

        prompt_path = os.path.join(prompts_dir_path, prompt_id)

        if not os.path.isdir(prompt_path):
            raise ValueError(
                f"Prompt {prompt_id} does not exist in project {project_id}"
            )

        prompt_config = self.get_prompt_config(project_id, prompt_id)

        return PromptModel.model_validate(
            {"id": prompt_id, **defaults, **prompt_config},
            context={"base_path": prompt_path},
        )
