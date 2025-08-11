import os

from prompting_workbench.domains.models.project import ProjectModel
from prompting_workbench.domains.repositories._core.fs_repository_base import (
    FileSystemRepositoryBase,
)


class ProjectRepository(FileSystemRepositoryBase):
    def __init__(self):
        super().__init__()

    def get_project(self, project_id) -> ProjectModel:
        project_path = os.path.join(self.projects_dir, project_id)

        if not os.path.isdir(project_path):
            raise ValueError(f"Project {project_id} does not exist")

        return ProjectModel(
            id=project_id,
        )
