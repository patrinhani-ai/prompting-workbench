from typing import Annotated, Optional
from prompting_workbench.core.models.types import ContentStrRenderer
from prompting_workbench.core.models.validators import py_validator_content_str_renderer
from pydantic import PlainSerializer, PlainValidator
from prompting_workbench.core.models.model_base import ModelBase


class PromptModel(ModelBase):
    """
    Prompt model for the prompting workbench.
    """

    id: str

    system: Annotated[
        ContentStrRenderer,
        PlainValidator(py_validator_content_str_renderer),
        PlainSerializer(lambda x: x.lazy_value, str),
    ] = ContentStrRenderer("")

    system_input: Optional[dict] = {}

    prompt: Annotated[
        ContentStrRenderer,
        PlainValidator(py_validator_content_str_renderer),
        PlainSerializer(lambda x: x.lazy_value, str),
    ] = ContentStrRenderer("")

    prompt_input: Optional[dict] = {}
