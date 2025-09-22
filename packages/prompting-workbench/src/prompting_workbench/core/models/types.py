import os
import re
from typing import Any, Literal

from prompting_workbench.core.utils.io import get_file_content

ContentStrRendererValueType = Literal["str", "file", "jinja"]


def _render_param_walk_handler(param: dict, ctx: dict) -> dict:
    result_input_dict: dict = param or {}

    for key, value in param.items():
        if isinstance(value, dict):
            result_input_dict[key] = _render_param_walk_handler(value, ctx)
        elif isinstance(value, str):
            result_input_dict[key] = _render_param_str_processor(value, key, ctx)

    return result_input_dict


def _render_param_str_processor(
    value: str, field_name: str | None, ctx: dict | None
) -> Any:
    base_path: str = "./"
    template_input: dict = {}
    input_field_name: str | None = f"{field_name}_input" if field_name else None

    if ctx is not None and input_field_name:
        base_path = ctx.get("base_path", "./")
        template_input = ctx.get(input_field_name, {})
        template_input = _render_param_walk_handler(template_input, ctx)

    # print(f"[_render_param_str_processor] field_name: {field_name}")
    # print(f"[_render_param_str_processor] value: {value}")
    # print(f"[_render_param_str_processor] base_path: {base_path}")
    # print(
    #     f"[_render_param_str_processor] template_input ({input_field_name}): {template_input}"
    # )

    if not value.startswith("<file"):
        return value

    re_match = re.search(r'<file src="(?P<file_path>[^"]*)"/>', value)

    if not re_match:
        return value

    field_value = value

    prompt_file_rel_path = re_match.group("file_path")

    if not prompt_file_rel_path:
        return value

    file_abs_path = os.path.join(base_path, prompt_file_rel_path)

    file_extension = os.path.splitext(file_abs_path)[1].lower()

    if file_extension in [".j2", ".jinja2"]:
        import jinja2

        template = jinja2.Template(get_file_content(file_abs_path))
        return template.render(**template_input)

    field_value = get_file_content(os.path.join(base_path, prompt_file_rel_path))

    return field_value


class ContentStrRenderer:
    lazy_value: str = ""
    value_type: ContentStrRendererValueType = "str"
    file_abs_path: str = ""
    render_params: dict = {}

    def __init__(self, lazy_value: str, base_path: str = "./"):
        self.lazy_value = lazy_value
        self.base_path = base_path

        self.value_type = self._identify_value_type()

    def _identify_value_type(self) -> ContentStrRendererValueType:
        value = self.lazy_value
        default_value_type: ContentStrRendererValueType = "str"

        if not value.startswith("<file"):
            return default_value_type

        re_match = re.search(r'<file src="(?P<file_path>[^"]*)"/>', value)

        if not re_match:
            return default_value_type

        prompt_file_rel_path = re_match.group("file_path")

        if not prompt_file_rel_path:
            return default_value_type

        self.file_abs_path = os.path.join(self.base_path, prompt_file_rel_path)

        file_extension = os.path.splitext(self.file_abs_path)[1].lower()

        if file_extension in [".j2", ".jinja2"]:
            return "jinja"
        else:
            return "file"

    def set_render_params(self, params: dict) -> None:
        self.render_params = params

    def _render_file(self) -> str:
        return get_file_content(self.file_abs_path)

    def _render_jinja(self, params: dict = None) -> str:
        import jinja2

        if params is None:
            params = {}

        template = jinja2.Template(get_file_content(self.file_abs_path))

        render_params = {**self.render_params, **params}

        render_params = _render_param_walk_handler(
            render_params, {"base_path": self.base_path}
        )

        return template.render(**render_params)

    def render(self, params: dict = None) -> str:
        if self.value_type == "file":
            return self._render_file()
        elif self.value_type == "jinja":
            return self._render_jinja(params)

        return self.lazy_value

    def __str__(self):
        return self.lazy_value

    def __repr__(self):
        return f"ContentStrRenderer({self.lazy_value})"

    @staticmethod
    def build(lazy_value: str, base_path: str = "./") -> "ContentStrRenderer":
        return ContentStrRenderer(lazy_value, base_path)
