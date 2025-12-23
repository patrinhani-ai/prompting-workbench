from abc import abstractmethod

from prompting_workbench.domains.project import Project
from prompting_workbench.domains.repositories._core.meta_config_fs_repository import (
    MetaConfigFileSystemRepository,
)
from prompting_workbench.domains.repositories._core.meta_config_repository_base import (
    MetaConfigRepositoryBase,
)
from prompting_workbench.domains.wrkbnch_context import WrkbnchContext

from blinker import signal


class BaseCliPlugin:
    meta_config_repository: MetaConfigRepositoryBase

    on_status_update = signal("on_status_update")

    def listen_on_status_update(self, handler):
        self.on_status_update.connect(handler)

    def disconnect_status_update(self, handler):
        self.on_status_update.disconnect(handler)

    def notify_status_update(self, key: str, status: str = "", text: str = ""):
        self.on_status_update.send(self, key=key, status=status, text=text)

    @property
    def context(self) -> WrkbnchContext:
        return WrkbnchContext.instance()

    @property
    def project(self) -> Project | None:
        return self.context.project

    def __init__(self):
        super().__init__()
        self.meta_config_repository = MetaConfigFileSystemRepository(
            plugin_instance=self
        )

    @abstractmethod
    def get_plugin_name(self):
        return "no_name"

    @abstractmethod
    def get_plugin_description(self):
        return "No description available"

    @abstractmethod
    def get_plugin_help(self):
        return "No help available"

    @abstractmethod
    def get_plugin_file_path(self):
        return __file__

    def get_plugin_command(self):
        return self.get_plugin_name()

    @abstractmethod
    def prepare(self, *args, **kwargs):
        self.context.update_data(**kwargs.get("context", {}))

    @abstractmethod
    def run(self):
        pass
