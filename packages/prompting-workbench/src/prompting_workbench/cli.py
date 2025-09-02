import os
import sys
import dotenv
import typer

from typing import List
from prompting_workbench.cli_engine_types import ICliEngine

from typing_extensions import Annotated


def dynamic_import_from_path(module_name, file_path):
    """
    Dynamically imports a Python module from a given file path.

    Args:
        module_name (str): The name to assign to the imported module.
        file_path (str): The full path to the Python module file (.py).

    Returns:
        module: The imported module object.
    """
    import importlib

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Add to sys.modules for standard import behavior
    spec.loader.exec_module(module)
    return module


CLI_EXTRA_HELP = """
Environment variables:

- PMPT_WRKBNCH_PROJECTS_DIR (default: ./wrkbnch_projects): Directory where the projects are stored,

Obs.: 

- all environment variable used by this tool must have the prefix 'PMPT_WRKBNCH_'.

- '.env' and '.env.wrkbnch' file is automatically loaded from the current directory by default if exists.

--------------------------------
"""

typer_app = typer.Typer(no_args_is_help=True, help=CLI_EXTRA_HELP)

cli_engine: ICliEngine


def setup():
    # Reload the variables in your '.env' file (override the existing variables)
    dotenv.load_dotenv(".env", override=True)


def _load_plugins_cli():
    global cli_engine, typer_app

    for plugin_name, plugin in cli_engine.plugins.items():
        plugin_file_path = plugin.get_plugin_file_path()
        plugin_src_folder = os.path.dirname(plugin_file_path)
        plugin_filename = os.path.basename(plugin_file_path)

        plugin_filename_no_ext = os.path.splitext(plugin_filename)[0]

        plugin_cli_path = os.path.join(
            plugin_src_folder, f"{plugin_filename_no_ext}_cli.py"
        )

        # dynamic load plugin module using importlib.import_module
        plugin_cli_module = dynamic_import_from_path(
            f"{plugin_filename_no_ext}_cli", plugin_cli_path
        )

        plugin_cli_module.plugin = plugin

        plugin_typer_app = plugin_cli_module.typer_app

        typer_app.add_typer(plugin_typer_app)

        # print(f"plugin_name: {plugin_name}")
        # print(f"plugin_file_path: {plugin_file_path}")
        # print(f"plugin_src_folder: {plugin_src_folder}")
        # print(f"plugin_filename: {plugin_filename}")
        # print(f"plugin_cli_path: {plugin_cli_path}")

        print(f"plugin_cli_module: {plugin_cli_module}")
        print(f"plugin_cli_module.plugin: {plugin_cli_module.plugin}")


@typer_app.callback(invoke_without_command=True)
def typer_callback(
    ctx: typer.Context,
    project: Annotated[
        str,
        typer.Option(
            metavar="PROJECT_NAME",
            max=1,
            help="Prompt Project name to load in the CLI context",
        ),
    ] = "NONE",
    prompts: Annotated[
        List[str],
        typer.Option(
            "--prompts",
            "-P",
            metavar="PROMPT_ID",
            help="List of prompts of the project to load in the CLI context",
        ),
    ] = [],
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            is_eager=True,
            help="Enable debug mode",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            is_eager=True,
            help="Enable dry-run mode",
        ),
    ] = False,
):
    print(f"[DEBUG] Project: {project}")
    print(f"[DEBUG] Prompts: {prompts}")
    print(f"[DEBUG] Debug: {debug}")
    print(f"[DEBUG] Dry Run: {dry_run}")
    print(f"[DEBUG] Context: {ctx}")

    global cli_engine
    cli_engine.start(project=project, prompts=prompts)

    ctx.obj = {
        **(dict(ctx.obj) if ctx.obj else {}),
        **(cli_engine.context.__dict__ or {}),
    }


def main():
    setup()

    WRKBNCH_TGGL_ENGINE_VERSION = os.getenv("WRKBNCH_TGGL_ENGINE_VERSION", "stable")

    print(f"Using Prompting Workbench Engine Version: {WRKBNCH_TGGL_ENGINE_VERSION}")

    from prompting_workbench.cli_engine import CliEngine

    global cli_engine
    cli_engine = CliEngine()

    cli_engine.prepare()

    _load_plugins_cli()

    typer_app()


if __name__ == "__main__":
    main()
