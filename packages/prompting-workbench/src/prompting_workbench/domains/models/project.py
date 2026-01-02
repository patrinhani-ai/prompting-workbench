from prompting_workbench.core.models.model_base import ModelBase


class ProjectModel(ModelBase):
    """
    Project model for the prompting workbench.
    """

    id: str

    name: str = ""
    description: str = ""
    version: str = "0.1.0"

    defaults: dict = {}
