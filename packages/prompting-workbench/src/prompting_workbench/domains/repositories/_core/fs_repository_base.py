from prompting_workbench.core.repositories.repository_base import RepositoryBase
from prompting_workbench.settings import settings


class FileSystemRepositoryBase(RepositoryBase):
    @property
    def projects_dir(self) -> str:
        return settings.projects_dir

    def __init__(self):
        super().__init__()
