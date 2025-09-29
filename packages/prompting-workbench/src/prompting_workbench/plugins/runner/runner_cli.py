from typing import Annotated
import typer
from rich.console import Console
from rich.progress import Progress

from prompting_workbench.plugins.runner.runner import RunnerCliPlugin

plugin: RunnerCliPlugin

typer_app = typer.Typer()
cmd_console = Console()

CONSOLE_LINE_LEN = 48


@typer_app.command()
def runner(
    ctx: typer.Context,
    output_folder: Annotated[
        str,
        typer.Option(
            max=1,
            help="Output folder for storing results",
        ),
    ] = "output",
):
    global plugin

    context: dict = dict(ctx.obj or {})

    plugin.prepare(context=context, output_folder=output_folder)

    cmd_console.rule("[ [magenta]Prompt Runner[/magenta] ]")
    cmd_console.print()
    cmd_console.print()

    progress = Progress(auto_refresh=True)
    progress.start()

    plugin.run()

    progress.stop()

    cmd_console.print()
    cmd_console.rule()
