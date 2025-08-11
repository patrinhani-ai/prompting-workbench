import argparse
import os
import textwrap
from typing import Any

from prompting_workbench.config import settings

from prompting_workbench.domains.project import Project
from prompting_workbench.wrkbnch_context import WrkbnchContext
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin
# from prompting_workbench.plugins import FlowWebCliPlugin
# from prompting_workbench.plugins.prompt_runner import (
#     PromptRunnerCliPlugin,
# )

CLI_EXTRA_HELP = """
Environment variables:

- PMPT_WRKBNCH_PROJECTS_DIR (default: ./wrkbnch_projects): Directory where the projects are stored,

Obs.: '.env' file is automatically loaded from the current directory by default.

--------------------------------
"""


class CliEngine:
    context: WrkbnchContext

    project: Project

    def __init__(self):
        self.plugins = {}
        self.context = WrkbnchContext()

    def _add_root_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "project",
            metavar="PROJECT_NAME",
            type=str,
            nargs="?",
            default="NONE",
            help="Prompt Project name to load in the CLI context",
        )

        parser.add_argument(
            "--prompts",
            "-P",
            type=str,
            nargs="*",
            default=[],
            help="List of prompts of the project to load in the CLI context",
        )

    def _add_common_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="Enable debug mode",
            required=False,
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Enable dry-run mode",
            required=False,
        )

        return parser

    def _load_plugin(
        self,
        subparsers: Any,
        plugin: BaseCliPlugin,
    ):
        plugin_name = plugin.get_plugin_name()

        if plugin_name in self.plugins:
            raise ValueError(f"Plugin with name '{plugin_name}' already loaded")

        plugin_parser = subparsers.add_parser(
            plugin.get_plugin_command(),
            description=plugin.get_plugin_description(),
            help=plugin.get_plugin_help(),
        )

        self._add_common_args(plugin_parser)

        plugin.set_plugin_arguments(plugin_parser)

        self.plugins[plugin_name] = plugin

    def _load_plugins(self, root_parser: argparse.ArgumentParser):
        pass  # TODO: Implement plugin loading logic
        # subparsers = root_parser.add_subparsers(
        #     title="Commands",
        #     dest="command",
        #     required=False,
        #     description="CLI commands",
        #     help="CLI commands",
        # )

        # self._load_plugin(subparsers, PromptRunnerCliPlugin(root_parser))

    def _load_project(self, project_id: str):
        if project_id == "NONE":
            print("No project specified.")

        self.project = Project.load(project_id)

    def _check_settings(self):
        if not settings.projects_dir:
            raise ValueError(
                "No projects directory specified. Please set the PMPT_WRKBNCH_PROJECTS_DIR environment variable."
            )

        if not os.path.exists(settings.projects_dir):
            raise ValueError(
                f"Projects directory '{settings.projects_dir}' does not exist."
            )

        print(f"[DEBUG] Projects directory: {settings.projects_dir}")

    def start(self):
        print("[DEBUG] Starting CLI Engine...")

        self._check_settings()

        root_parser = argparse.ArgumentParser(
            description="Prompting Workbench CLI for FLOW multi-threading task execution and integrations.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(CLI_EXTRA_HELP),
        )

        self._add_root_args(root_parser)

        self._load_plugins(root_parser)

        args = root_parser.parse_args()

        print(f"[DEBUG] Arguments: {args}")
        print(f"[DEBUG] cmd: {args.command}")

        print("-" * 40)

        self._load_project(args.project)

        print("-" * 40)

        self.project.load_prompts(list(set(args.prompts)))

        arg__command = args.command or "default"

        if arg__command != "default" and arg__command in self.plugins:
            plugin: BaseCliPlugin = self.plugins.get(arg__command)

            plugin.prepare()
            # return

            plugin.run()
