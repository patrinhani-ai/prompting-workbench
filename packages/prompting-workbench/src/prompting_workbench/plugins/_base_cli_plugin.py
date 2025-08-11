import argparse
import datetime
import os
from abc import abstractmethod

from prompting_workbench.domains.project import Project


class BaseCliPlugin:
    root_parser: argparse.ArgumentParser
    project: Project
    context: dict
    cli_args: argparse.Namespace

    @property
    def arg__debug(self):
        return self.cli_args.debug

    @property
    def arg__dry_run(self):
        return self.cli_args.dry_run

    @property
    def arg__project_prompts(self):
        return self.cli_args.prompts or []

    @property
    def output_target_path(self):
        return self.context.get("target_project_dir", self.cli_args.output_folder)

    def __init__(self, root_parser: argparse.ArgumentParser):
        super().__init__()
        self.context = {}
        self.cli_args = argparse.Namespace()
        self.root_parser = root_parser

    @abstractmethod
    def get_plugin_name(self):
        return self.plugin_name

    @abstractmethod
    def get_plugin_description(self):
        return "No description available"

    @abstractmethod
    def get_plugin_help(self):
        return "No help available"

    def get_plugin_command(self):
        return self.get_plugin_name()

    def set_plugin_arguments(self, parser: argparse.ArgumentParser):
        return parser

    def prepare(self):
        self.cli_args = self.root_parser.parse_args()

        arg__project_name = self.cli_args.project or "NONE"
        arg__output_folder = self.cli_args.output_folder or "output"
        arg__project_name = self.cli_args.project

        if arg__project_name != "NONE":
            self.project = Project.load_from_store(arg__project_name)

        init_timestamp_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.context = {
            "init_timestamp_str": init_timestamp_str,
            "target_project_dir": os.path.join(
                arg__output_folder,
                "prompting_workbench",
                self.get_plugin_command(),
                arg__project_name,
                init_timestamp_str,
            ),
        }

    @abstractmethod
    def run(self):
        pass
