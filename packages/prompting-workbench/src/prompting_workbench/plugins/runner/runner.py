from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin
from prompting_workbench.plugins.runner.domains.runner_controller import (
    RunnerPluginController,
)


class RunnerCliPlugin(BaseCliPlugin):
    runner_controller: RunnerPluginController

    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return "runner"

    def get_plugin_description(self):
        return "Run prompts of specified project"

    def get_plugin_help(self):
        return "Run prompts of specified project"

    def get_plugin_file_path(self):
        return __file__

    # def set_plugin_arguments(self, plugin_parser: argparse.ArgumentParser):
    #     plugin_parser.add_argument(
    #         "--output_folder",
    #         type=str,
    #         nargs="?",
    #         default="output",
    #         help="Output folder for storing results",
    #     )

    #     plugin_parser.add_argument(
    #         "--test",
    #         action="store_true",
    #         default=False,
    #         help="Enable test mode",
    #         required=False,
    #     )

    #     return plugin_parser

    def prepare(self, context: dict, output_folder: str):
        super().prepare(context=context)

        if not self.project:
            print(f"[ERROR][{self.get_plugin_name()}] No project found.")
            return

        self.runner_controller = RunnerPluginController(
            plugin=self,
            project=self.project,
            context=self.context,
            output_folder=output_folder,
            meta_config_repository=self.meta_config_repository,
        )

        # print(
        #     f"[DEBUG][{self.get_plugin_name()}] Prepared plugin with output folder: {self.output_folder}"
        # )

    def run(self):
        self.runner_controller.run_parallel()

    def __repr__(self):
        return f"<{self.__class__.__name__} output_folder={self.runner_controller.output_folder}>"
