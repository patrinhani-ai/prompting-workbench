from typing import Optional

from prompting_workbench.core.models.model_base import ModelBase

"""
{
  "llm_provider": "openai",
  "llm_model": "gpt-4o",
  "temperature": 1.5,
  "llm_custom_params": {},
  "system_input": {},
  "prompt_input": {},
  "attachments": [],
  "tasks": [
    {
      "llm_provider": "google_genai",
      "llm_model": "gemini-2.0-flash",
      "temperature": 1.5
    },
    {
      "llm_provider": "google_genai",
      "llm_model": "gemini-2.0-flash",
      "temperature": 0.8
    }
  ]
}
"""


class RunnerExecutionPlanTask(ModelBase):
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    temperature: Optional[float] = None
    llm_custom_params: Optional[dict] = None
    system_input: Optional[dict] = None
    prompt_input: Optional[dict] = None
    attachments: Optional[list] = None


class RunnerExecutionPlan(ModelBase):
    """
    Execution plan model for the prompting workbench runner plugin.
    """

    id: Optional[str] = None
    llm_provider: Optional[str] = "openai"
    llm_model: Optional[str] = "gpt-4o"
    temperature: Optional[float] = 1.0
    llm_custom_params: Optional[dict] = {}
    system_input: Optional[dict] = {}
    prompt_input: Optional[dict] = {}
    attachments: Optional[list] = []
    tasks: Optional[
        list[RunnerExecutionPlanTask]
    ] = []  # List of task-specific overrides
