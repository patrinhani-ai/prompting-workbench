from datetime import datetime
import os
import random
import time
from prompting_workbench.domains.project import Project
from prompting_workbench.domains.prompt import Prompt
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin


class RunnerPluginTask:
    task_key: str
    output_folder: str
    project: Project
    prompt: Prompt
    plugin: BaseCliPlugin

    debug: bool = False
    dry_run: bool = False

    def __init__(
        self,
        task_key: str,
        project: Project,
        prompt: Prompt,
        plugin: BaseCliPlugin,
        output_folder: str,
        debug: bool = False,
        dry_run: bool = False,
    ):
        self.task_key = task_key
        self.project = project
        self.prompt = prompt
        self.plugin = plugin
        self.output_folder = output_folder
        self.debug = debug
        self.dry_run = dry_run

    def _prepare_output_dir(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        output_dir = os.path.join(
            self.output_folder,
            self.plugin.get_plugin_name(),
            f"{self.task_key}--{timestamp}",
        )

        if self.debug:
            print(f"[DEBUG] Output directory: {output_dir}")

        if self.dry_run:
            print("[DRY RUN] Skipping output directory creation...")
            return output_dir

        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def run(self):
        self.plugin.notify_status_update(
            key=self.task_key,
            status="running",
            text="LLM runner task started...",
        )

        output_run_task_dir = self._prepare_output_dir()

        print(f"Running LLM runner task... Output dir: {output_run_task_dir}")

        # DEBUG: Print prompt details
        print(f"[DEBUG] Project ID: {self.project.project_id}")
        print(f"[DEBUG] Project Data: {self.project.data}")

        print("-" * 80)

        print(f"[DEBUG] Prompt ID: {self.prompt.prompt_id}")

        print(f"[DEBUG] Prompt System: {self.prompt.data.system}")
        print(f"[DEBUG] Prompt System Path: {self.prompt.data.system.file_abs_path}")
        print(f"[DEBUG] Prompt System Lazy Value: {self.prompt.data.system.render()}")

        print(f"[DEBUG] Prompt Content: {self.prompt.data.prompt}")
        print(f"[DEBUG] Prompt Content Path: {self.prompt.data.prompt.file_abs_path}")
        print(f"[DEBUG] Prompt Content Lazy Value: {self.prompt.data.prompt.render()}")

        time.sleep(random.uniform(4, 8))

        self.plugin.notify_status_update(
            key=self.task_key,
            status="done",
            text="LLM runner task completed.",
        )


def llm_runner_task(
    task_key: str,
    project: Project,
    prompt: Prompt,
    output_folder: str,
    plugin: BaseCliPlugin,
    debug: bool = False,
    dry_run: bool = False,
):
    # print("[DEBUG] Running LLM runner task...")
    # print(f"[DEBUG] Task key: {task_key}")
    # print(f"[DEBUG] Output folder: {output_folder}")
    # print(f"[DEBUG] Project: {project}")
    # print(f"[DEBUG] Prompt: {prompt}")
    # print(f"[DEBUG] Debug mode: {debug}")
    # print(f"[DEBUG] Dry run mode: {dry_run}")

    task = RunnerPluginTask(
        task_key=task_key,
        project=project,
        prompt=prompt,
        plugin=plugin,
        output_folder=output_folder,
        debug=debug,
        dry_run=dry_run,
    )

    task.run()
