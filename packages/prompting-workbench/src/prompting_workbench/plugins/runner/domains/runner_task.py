import logging
import os
from datetime import datetime

from prompting_workbench.core.llm.llm_chat import (
    LLMChatModelParams,
    LLMRunConfig,
    llm_chat_invoke,
)
from prompting_workbench.core.utils.io import write_file, write_json_file
from prompting_workbench.domains.project import Project
from prompting_workbench.domains.prompt import Prompt
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

from .models.execution_plan import (
    RunnerExecutionPlan,
)


class RunnerPluginTask:
    task_key: str
    output_folder: str
    project: Project
    prompt: Prompt
    prompt_exec_plan: RunnerExecutionPlan
    plugin: BaseCliPlugin

    debug: bool = False
    dry_run: bool = False

    def __init__(
        self,
        task_key: str,
        project: Project,
        prompt: Prompt,
        prompt_exec_plan: RunnerExecutionPlan,
        plugin: BaseCliPlugin,
        output_folder: str,
        debug: bool = False,
        dry_run: bool = False,
    ):
        self.task_key = task_key
        self.project = project
        self.prompt = prompt
        self.prompt_exec_plan = prompt_exec_plan
        self.plugin = plugin
        self.output_folder = output_folder
        self.debug = debug
        self.dry_run = dry_run

    def _prepare_output_dir(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        output_dir = os.path.join(
            self.output_folder,
            self.plugin.get_plugin_name(),
            self.project.project_id,
            f"{self.task_key}--{timestamp}",
        )

        if self.debug:
            logging.debug(f"Output directory: {output_dir}")

        if self.dry_run:
            print("[DRY RUN] Skipping output directory creation...")
            return output_dir

        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _output_write_llm_result(self, output_run_task_dir: str, llm_result):
        write_file(
            os.path.join(output_run_task_dir, "llm_result-content.md"),
            str(llm_result.content),
        )

        write_json_file(
            os.path.join(output_run_task_dir, "llm_result-resp_metadata.json"),
            llm_result.response_metadata,
        )

        write_json_file(
            os.path.join(output_run_task_dir, "llm_result-usage_metadata.json"),
            llm_result.usage_metadata,
        )

    def run(self):
        self.plugin.notify_status_update(
            key=self.task_key,
            status="running",
            text="LLM runner task started...",
        )

        output_run_task_dir = self._prepare_output_dir()

        logging.info(f"Running LLM runner task... Output dir: {output_run_task_dir}")

        prompt = self.prompt
        prompt_exec_plan = self.prompt_exec_plan

        system_input = {
            **(prompt.data.system_input or {}),
            **(prompt_exec_plan.system_input or {}),
        }

        system_msg_text = prompt.data.system.render(system_input)

        if self.debug:
            write_file(
                os.path.join(output_run_task_dir, "system_message.debug.md"),
                system_msg_text,
            )

        prompt_input = {
            **(prompt.data.prompt_input or {}),
            **(prompt_exec_plan.prompt_input or {}),
        }

        human_msg_text = prompt.data.prompt.render(prompt_input)

        if self.debug:
            write_file(
                os.path.join(output_run_task_dir, "human_message.debug.md"),
                human_msg_text,
            )

        llm_result = llm_chat_invoke(
            system_msg_text=system_msg_text,
            human_msg_text=human_msg_text,
            model_params=LLMChatModelParams(
                llm_provider=prompt_exec_plan.llm_provider,
                llm_model=prompt_exec_plan.llm_model,
                temperature=prompt_exec_plan.temperature,
            ),
            run_config=LLMRunConfig(
                run_name=f"runner_task--{self.task_key}",
            ),
        )

        self._output_write_llm_result(output_run_task_dir, llm_result)

        self.plugin.notify_status_update(
            key=self.task_key,
            status="done",
            text="LLM runner task completed.",
        )


def llm_runner_task(
    task_key: str,
    project: Project,
    prompt: Prompt,
    prompt_exec_plan: RunnerExecutionPlan,
    output_folder: str,
    plugin: BaseCliPlugin,
    debug: bool = False,
    dry_run: bool = False,
):
    task = RunnerPluginTask(
        task_key=task_key,
        project=project,
        prompt=prompt,
        prompt_exec_plan=prompt_exec_plan,
        plugin=plugin,
        output_folder=output_folder,
        debug=debug,
        dry_run=dry_run,
    )

    task.run()
