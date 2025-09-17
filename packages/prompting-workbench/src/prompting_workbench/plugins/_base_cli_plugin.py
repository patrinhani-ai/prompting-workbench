from abc import abstractmethod

from prompting_workbench.domains.project import Project
from prompting_workbench.wrkbnch_context import WrkbnchContext

from blinker import signal


class BaseCliPlugin:
    context: WrkbnchContext

    on_status_update = signal("on_status_update")

    def listen_on_status_update(self, handler):
        self.on_status_update.connect(handler)

    def disconnect_status_update(self, handler):
        self.on_status_update.disconnect(handler)

    def notify_status_update(self, key: str, status: str = "", text: str = ""):
        self.on_status_update.send(self, key=key, status=status, text=text)

    @property
    def project(self) -> Project | None:
        return self.context.project

    # output_folder: str

    # @property
    # def arg__debug(self):
    #     return self.cli_args.debug

    # @property
    # def arg__dry_run(self):
    #     return self.cli_args.dry_run

    # @property
    # def arg__project_prompts(self):
    #     return self.cli_args.prompts or []

    # @property
    # def output_target_path(self):
    #     return self.context.get("target_project_dir", self.output_folder)

    def __init__(self):
        super().__init__()
        self.context = WrkbnchContext()

    def set_context(self, **kargs):
        self.context = WrkbnchContext(**kargs)

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
        self.set_context(**kwargs.get("context", {}))

    @abstractmethod
    def run(self):
        pass
