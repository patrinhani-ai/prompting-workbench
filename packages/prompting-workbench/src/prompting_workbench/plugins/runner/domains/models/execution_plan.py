from prompting_workbench.core.models.model_base import ModelBase


class RunnerExecutionPlan(ModelBase):
    """
    Execution plan model for the prompting workbench runner plugin.
    """

    id: str
    defaults: dict = {}
