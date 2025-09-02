from typing import Annotated
import typer

from prompting_workbench.plugins.runner.runner import RunnerCliPlugin

plugin: RunnerCliPlugin

typer_app = typer.Typer()


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

    plugin.run()
