from typing import Annotated
import typer
from rich.console import Console
from rich.table import Table

from prompting_workbench.plugins.config.config import ConfigCliPlugin

plugin: ConfigCliPlugin

typer_app = typer.Typer()
cmd_console = Console()


@typer_app.command()
def config(
    ctx: typer.Context,
    view: Annotated[
        bool,
        typer.Option(
            "--view",
            help="Display current configuration settings",
        ),
    ] = False,
):
    """View and manage configuration settings"""
    global plugin

    context: dict = dict(ctx.obj or {})

    plugin.prepare(context=context)

    if view:
        cmd_console.rule("[ [magenta]Configuration Settings[/magenta] ]")
        cmd_console.print()

        config_data = plugin.run()

        # Create a table for better formatting
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="green", width=30)
        table.add_column("Value", style="yellow")

        # Add each configuration setting to the table
        for key, value in config_data.items():
            # Format the key to be more readable
            display_key = key.replace("_", " ").title()
            table.add_row(display_key, str(value))

        cmd_console.print(table)
        cmd_console.print()
        cmd_console.rule()
    else:
        cmd_console.print(
            "[yellow]Use --view to display configuration settings[/yellow]"
        )
        cmd_console.print()
        cmd_console.print("Example: prompting-workbench config --view")
