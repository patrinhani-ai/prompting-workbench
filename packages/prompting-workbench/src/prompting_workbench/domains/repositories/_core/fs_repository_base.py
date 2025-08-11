from prompting_workbench.config import settings

from .repository_base import (
    RepositoryBase,
)


class FileSystemRepositoryBase(RepositoryBase):
    projects_dir: str

    def __init__(self):
        super().__init__()

        self.projects_dir = settings.projects_dir
