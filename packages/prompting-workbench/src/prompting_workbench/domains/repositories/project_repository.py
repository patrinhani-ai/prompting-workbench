import os

from prompting_workbench.core.utils.io import get_json_content
from prompting_workbench.domains.models.project import ProjectModel
from prompting_workbench.domains.repositories._core.fs_repository_base import (
    FileSystemRepositoryBase,
)


class ProjectRepository(FileSystemRepositoryBase):
    def __init__(self):
        super().__init__()

    def _get_project_dir(self, project_id: str) -> str:
        if (not project_id) or (project_id.strip() == ""):
            return os.path.join(self.projects_dir)

        return os.path.join(self.projects_dir, project_id)

    def get_project_config_path(self, project_id) -> str:
        project_dir = self._get_project_dir(project_id)

        if not os.path.isdir(project_dir):
            raise ValueError(f"Project {project_id} does not exist")

        project_config_dir_path = os.path.join(project_dir, ".config")
        project_config_path = os.path.join(project_config_dir_path, "meta_info.json")

        if not os.path.isfile(project_config_path):
            raise ValueError(f"Project config for project {project_id} does not exist")

        return project_config_path

    def get_project_config(self, project_id) -> dict:
        project_config_path = self.get_project_config_path(project_id)

        if not os.path.isfile(project_config_path):
            raise ValueError(f"Project config for project {project_id} does not exist")

        return get_json_content(project_config_path)

    def get_project(self, project_id) -> ProjectModel:
        if (not project_id) or (project_id.strip() == ""):
            project_path = os.path.join(self.projects_dir)
        else:
            project_path = os.path.join(self.projects_dir, project_id)

        if not os.path.isdir(project_path):
            raise ValueError(f"Project {project_id} does not exist")

        project_config = self.get_project_config(project_id)

        return ProjectModel.model_validate(
            {"id": project_id, **project_config}, context={"base_path": project_path}
        )
