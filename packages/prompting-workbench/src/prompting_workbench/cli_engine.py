import os

from prompting_workbench.cli_engine_types import ICliEngine
from prompting_workbench.config import settings

from prompting_workbench.domains.project import Project
from prompting_workbench.wrkbnch_context import WrkbnchContext

from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

# from prompting_workbench.plugins import FlowWebCliPlugin
# from prompting_workbench.plugins.prompt_runner import (
#     PromptRunnerCliPlugin,
# )


class CliEngine(ICliEngine):
    plugins: dict[str, BaseCliPlugin]
    context: WrkbnchContext

    project: Project

    def __init__(self):
        self.plugins: dict[str, BaseCliPlugin] = {}
        self.context = WrkbnchContext()

    def _load_plugin(
        self,
        plugin: BaseCliPlugin,
    ):
        plugin_name = plugin.get_plugin_name()

        if plugin_name in self.plugins:
            raise ValueError(f"Plugin with name '{plugin_name}' already loaded")

        self.plugins[plugin_name] = plugin

    def _load_plugins(self):
        # pass
        from prompting_workbench.plugins.runner.runner import (
            RunnerCliPlugin,
        )

        self._load_plugin(RunnerCliPlugin())

    def _load_project(self, project_id: str):
        if project_id == "NONE":
            project_id = ""

        self.project = Project.load(project_id)
        self.context.project = self.project

    def _check_settings(self):
        if not settings.projects_dir:
            raise ValueError(
                "No projects directory specified. Please set the PMPT_WRKBNCH_PROJECTS_DIR environment variable."
            )

        if not os.path.exists(settings.projects_dir):
            raise ValueError(
                f"Projects directory '{settings.projects_dir}' does not exist."
            )

        # print(f"[DEBUG] Projects directory: {settings.projects_dir}")

    def prepare(self):
        # print("[DEBUG] Preparing CLI Engine...")
        self._check_settings()

        self._load_plugins()

    def start(self, project: str, prompts: list[str]):
        # print("[DEBUG] Starting CLI Engine...")
        self._load_project(project)
        self.project.load_prompts(list(set(prompts)))

        # arg__command = args.command or "default"

        # if arg__command != "default" and arg__command in self.plugins:
        #     plugin: BaseCliPlugin = self.plugins.get(arg__command)

        #     plugin.prepare()
        #     # return

        #     plugin.run()
