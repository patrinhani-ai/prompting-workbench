import random
import time
from prompting_workbench.domains.project import Project
from prompting_workbench.domains.prompt import Prompt
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin


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
    plugin.notify_status_update(
        key=task_key,
        status="running",
        text="======> LLM runner task started...",
    )
    time.sleep(random.uniform(4, 8))
    plugin.notify_status_update(
        key=task_key,
        status="done",
        text="======> LLM runner task completed.",
    )
