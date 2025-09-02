from .._base_cli_plugin import BaseCliPlugin

# from .tasks import PromptTestRunner, task_llm_runner


class RunnerCliPlugin(BaseCliPlugin):
    output_folder: str

    @property
    def output_target_path(self):
        return self.context.get("target_project_dir", self.output_folder)

    def __init__(self):
        super().__init__()
        self.output_folder = "output"

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

        self.output_folder = output_folder

        print(
            f"[DEBUG][{self.get_plugin_name()}] Prepared plugin with output folder: {self.output_folder}"
        )

    def run(self):
        print(
            f"[DEBUG][{self.get_plugin_name()}] Running plugin: {self.get_plugin_name()}..."
        )
        print(f"[DEBUG][{self.get_plugin_name()}] Running with context: {self.context}")

    def __repr__(self):
        return f"<{self.__class__.__name__} output_folder={self.output_folder}>"
