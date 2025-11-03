from datetime import datetime
import os
import random
import time
from prompting_workbench.domains.project import Project
from prompting_workbench.domains.prompt import Prompt
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

from .models.execution_plan import (
    RunnerExecutionPlan,
)

from langchain_core.runnables.config import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model


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

        # # DEBUG: Print prompt details
        # print(f"[DEBUG] Project ID: {self.project.project_id}")
        # print(f"[DEBUG] Project Data: {self.project.data}")

        # print("-" * 80)

        # print(f"[DEBUG] Prompt ID: {self.prompt.prompt_id}")

        # print(f"[DEBUG] Prompt System: {self.prompt.data.system}")
        # print(f"[DEBUG] Prompt System Path: {self.prompt.data.system.file_abs_path}")
        # print(f"[DEBUG] Prompt System Lazy Value: {self.prompt.data.system.render()}")

        # print(f"[DEBUG] Prompt Content: {self.prompt.data.prompt}")
        # print(f"[DEBUG] Prompt Content Path: {self.prompt.data.prompt.file_abs_path}")
        # print(f"[DEBUG] Prompt Content Lazy Value: {self.prompt.data.prompt.render()}")

        prompt = self.prompt
        prompt_exec_plan = self.prompt_exec_plan

        # print(
        #     f"===========> [DEBUG][] Loaded execution plan for prompt {prompt.prompt_id}: {prompt_exec_plan}"
        # )

        prompt_template = ChatPromptTemplate(
            messages=[
                SystemMessage(prompt.data.system.render()),
                HumanMessage(prompt.data.prompt.render()),
            ]
        )

        llm_model = init_chat_model(
            model_provider=prompt_exec_plan.llm_provider,
            model=prompt_exec_plan.llm_model,
            temperature=prompt_exec_plan.temperature,
        )

        llm_chain = prompt_template | llm_model

        from langchain_core.globals import set_debug

        set_debug(True)

        llm_result = llm_chain.invoke(
            input={},
            config=RunnableConfig(
                run_name=f"runner_task--{self.task_key}",
            ),
        )

        set_debug(False)

        print("LLM Result:")
        print("-" * 80)
        print(llm_result)
        print("-" * 80)

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
        prompt_exec_plan=prompt_exec_plan,
        plugin=plugin,
        output_folder=output_folder,
        debug=debug,
        dry_run=dry_run,
    )

    task.run()
