import concurrent

from .domains.runner_task import llm_runner_task
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

        # print(
        #     f"[DEBUG][{self.get_plugin_name()}] Prepared plugin with output folder: {self.output_folder}"
        # )

    def run(self):
        # print(
        #     f"[DEBUG][{self.get_plugin_name()}] Running plugin: {self.get_plugin_name()}..."
        # )
        # print(f"[DEBUG][{self.get_plugin_name()}] Running with context: {self.context}")
        project = self.project

        if not project:
            print(f"[ERROR][{self.get_plugin_name()}] No project found.")
            return

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            task_idx = 0
            for prompt in project.prompts:
                prompt_id = prompt.prompt_id
                task_key = f"{prompt_id}-task_{task_idx}"
                futures.append(
                    executor.submit(
                        llm_runner_task,
                        task_key,
                        project,
                        prompt,
                        self.output_folder,
                        self,
                        self.context.debug,
                        self.context.dry_run,
                    )
                )
                task_idx += 1

            for future in concurrent.futures.as_completed(futures):
                future.result()

    def __repr__(self):
        return f"<{self.__class__.__name__} output_folder={self.output_folder}>"
