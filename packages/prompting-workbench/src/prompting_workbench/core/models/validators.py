# import os
# import re
from typing import Any

# from prompting_workbench.core.utils.io import get_file_content
from pydantic import ValidationInfo

from .types import ContentStrRenderer, _render_param_walk_handler


# def py_validator_str_advcd(value: str, info: ValidationInfo) -> Any:
#     return _validator_str_advcd(value, info.field_name, info.context)


# def _validator_str_advcd(value: str, field_name: str | None, ctx: dict | None) -> Any:
#     base_path: str = "./"
#     template_input: dict = {}
#     input_field_name: str | None = f"{field_name}_input" if field_name else None

#     if ctx is not None and input_field_name:
#         base_path = ctx.get("base_path", "./")
#         template_input = ctx.get(input_field_name, {})
#         template_input = _input_field_dict_walk_handler(template_input, ctx)

#     # print(f"[DEBUG] [py_validator_str_advcd] field_name: {field_name}")
#     # print(f"[DEBUG] [py_validator_str_advcd] value: {value}")
#     # print(f"[DEBUG] [py_validator_str_advcd] base_path: {base_path}")
#     # print(
#     #     f"[DEBUG] [py_validator_str_advcd] template_input ({input_field_name}): {template_input}"
#     # )

#     if not value.startswith("<file"):
#         return value

#     re_match = re.search(r'<file src="(?P<file_path>[^"]*)"/>', value)

#     if not re_match:
#         return value

#     field_value = value

#     prompt_file_rel_path = re_match.group("file_path")

#     if not prompt_file_rel_path:
#         return value

#     file_abs_path = os.path.join(base_path, prompt_file_rel_path)

#     file_extension = os.path.splitext(file_abs_path)[1].lower()

#     if file_extension in [".j2", ".jinja2"]:
#         import jinja2

#         template = jinja2.Template(get_file_content(file_abs_path))
#         return template.render(**template_input)

#     field_value = get_file_content(os.path.join(base_path, prompt_file_rel_path))

#     return field_value


# def _input_field_dict_walk_handler(input_dict: dict, ctx: dict) -> dict:
#     result_input_dict: dict = input_dict or {}

#     for key, value in input_dict.items():
#         if isinstance(value, dict):
#             result_input_dict[key] = _input_field_dict_walk_handler(value, ctx)
#         elif isinstance(value, str):
#             result_input_dict[key] = _validator_str_advcd(value, key, ctx)

#     return result_input_dict


def py_validator_content_str_renderer(value: str, info: ValidationInfo) -> Any:
    base_path: str = "./"
    template_input: dict = {}
    field_name = info.field_name
    ctx = info.context

    input_field_name: str | None = f"{field_name}_input" if field_name else None

    if ctx is not None and input_field_name:
        base_path = ctx.get("base_path", "./")
        template_input = ctx.get(input_field_name, {})
        # template_input = _input_field_dict_walk_handler(template_input, ctx)
        template_input = _render_param_walk_handler(template_input, ctx)

    field_content_renderer = ContentStrRenderer.build(value, base_path)

    field_content_renderer.set_render_params(template_input)

    # print("*".strip() * 80)
    # print(f"[DEBUG] [py_validator_content_str_renderer] field_name: {field_name}")

    # print(f"[DEBUG] [ContentStrRenderer] value: {field_content_renderer.lazy_value}")
    # print(f"[DEBUG] [ContentStrRenderer] value_type: {field_content_renderer.value_type}")
    # print(f"[DEBUG] [ContentStrRenderer] render_params: {field_content_renderer.render_params}")

    # print("*".strip() * 80)

    return field_content_renderer
