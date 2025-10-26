from prompting_workbench.domains.project import Project
from prompting_workbench.domains.prompt import Prompt
from prompting_workbench.domains.repositories._core.meta_config_repository_base import (
    MetaConfigRepositoryBase,
)
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin
from prompting_workbench.plugins.runner.domains.models.execution_plan import (
    RunnerExecutionPlan,
)
from prompting_workbench.plugins.runner.domains.runner_task import llm_runner_task
from prompting_workbench.wrkbnch_context import WrkbnchContext


class RunnerPluginController:
    output_folder: str
    plugin: BaseCliPlugin
    project: Project
    context: WrkbnchContext
    meta_config_repository: MetaConfigRepositoryBase

    @property
    def output_target_path(self):
        return self.context.get("target_project_dir", self.output_folder)

    def __init__(
        self,
        plugin: BaseCliPlugin,
        project: Project,
        context: WrkbnchContext,
        meta_config_repository: MetaConfigRepositoryBase,
        output_folder: str = "output",
    ):
        self.plugin = plugin
        self.project = project
        self.context = context
        self.output_folder = output_folder
        self.meta_config_repository = meta_config_repository

    EXEC_PLAN_CONFIG_NAME = "execution_plan"

    def _load_execution_plan_defaults(self) -> dict:
        proj_exec_plan_dict = (
            self.meta_config_repository.get_project_plugin_meta_config(
                self.EXEC_PLAN_CONFIG_NAME
            )
        )

        return proj_exec_plan_dict

    def _load_prompt_execution_plan(self, prompt: Prompt) -> RunnerExecutionPlan:
        exec_plan_defaults = self._load_execution_plan_defaults()

        prompt_exec_plan_dict = (
            self.meta_config_repository.get_prompt_plugin_meta_config(
                prompt.prompt_id, self.EXEC_PLAN_CONFIG_NAME
            )
        )

        merged_dict = {
            "id": prompt_exec_plan_dict.get("id", prompt.prompt_id),
            **exec_plan_defaults,
            **prompt_exec_plan_dict,
        }

        return RunnerExecutionPlan.model_validate(merged_dict)

    def run_parallel(self):
        import concurrent

        project = self.project

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            arg_debug = self.context.debug
            arg_dry_run = self.context.dry_run

            print(
                f"[DEBUG][] Starting parallel execution for project {project.project_id} with debug={arg_debug} and dry_run={arg_dry_run}"
            )

            task_idx = 0
            for prompt in project.prompts:
                prompt_id = prompt.prompt_id
                task_key = f"{prompt_id}-task_{task_idx}"
                prompt_exec_plan = self._load_prompt_execution_plan(prompt)

                print(
                    f"===========> [DEBUG][] Loaded execution plan for prompt {prompt_id}: {prompt_exec_plan}"
                )

                futures.append(
                    executor.submit(
                        llm_runner_task,
                        task_key,
                        project,
                        prompt,
                        self.output_folder,
                        self.plugin,
                        arg_debug,
                        arg_dry_run,
                    )
                )
                task_idx += 1

            for future in concurrent.futures.as_completed(futures):
                future.result()
