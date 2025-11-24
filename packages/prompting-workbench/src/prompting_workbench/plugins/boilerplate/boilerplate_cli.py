import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table

from prompting_workbench.config import settings
from prompting_workbench.plugins.boilerplate.boilerplate import BoilerplateCliPlugin
from prompting_workbench.plugins.boilerplate.domains.boilerplate_generator import (
    BoilerplateGenerator,
)

typer_app = typer.Typer(help="Generate boilerplate code for projects and prompts")
plugin: BoilerplateCliPlugin  # noqa: F821  # Injected by CLI engine at runtime

console = Console()


@typer_app.command("wb-list-templates")
def list_templates():
    """
    List available templates and examples.
    """
    console.print()
    console.rule("[bold cyan]Available Templates[/bold cyan]")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Example", style="yellow")

    table.add_row(
        "Project", "Basic project structure", "boilerplate create-project my_project"
    )
    table.add_row(
        "Prompt",
        "Basic prompt with system/user templates",
        "boilerplate create-prompt my_project 01-01 my_prompt",
    )

    console.print(table)
    console.print()

    console.print("[bold cyan]LLM Providers:[/bold cyan]")
    console.print("  • openai    - OpenAI models (gpt-4, gpt-4o-mini, etc.)")
    console.print("  • anthropic - Anthropic models (claude-3-opus, etc.)")
    console.print("  • ollama    - Local models via Ollama")
    console.print()


@typer_app.command("wb-create-project")
def create_project(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Project name")],
    description: Annotated[
        str, typer.Option("--description", "-d", help="Project description")
    ] = "Project description",
):
    """
    Create a new project with proper structure.

    Example:
        prompting_workbench boilerplate create-project my_project
    """
    global plugin  # noqa: F821

    context: dict = dict(ctx.obj or {})

    plugin.prepare(context=context)

    plugin.notify_status_update(
        key="create-project", status="running", text=f"Creating project: {name}"
    )

    try:
        generator = BoilerplateGenerator(settings.projects_dir)
        project_path = generator.create_project(name, description)

        plugin.notify_status_update(
            key="create-project", status="done", text=f"Project created: {project_path}"
        )

        console.print()
        console.rule("[bold green]Project Created Successfully[/bold green]")
        console.print()
        console.print(f"[green]✓[/green] Project: [bold]{name}[/bold]")
        console.print(f"[green]✓[/green] Location: [bold]{project_path}[/bold]")
        console.print()
        console.print("[bold cyan]Next steps:[/bold cyan]")
        console.print("  1. Create your first prompt:")
        console.print(
            f"     [yellow]prompting_workbench boilerplate create-prompt {name} 01-01 my_first_prompt[/yellow]"
        )
        console.print()

    except ValueError as e:
        plugin.notify_status_update(key="create-project", status="error", text=str(e))
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)


@typer_app.command("wb-create-prompt")
def create_prompt(
    ctx: typer.Context,
    prompt_id: Annotated[
        str, typer.Argument(help="Prompt ID (format: NN-NN, e.g., 01-03)")
    ],
    name: Annotated[str, typer.Argument(help="Prompt name (e.g., greeting_assistant)")],
    project: Annotated[
        str,
        typer.Option(
            "--project",
            "-p",
            help="Project name (optional if using --project flag at root)",
        ),
    ] = None,
    system_prompt: Annotated[
        str, typer.Option("--system", "-s", help="Custom system prompt")
    ] = None,
    user_prompt: Annotated[
        str, typer.Option("--user", "-u", help="Custom user prompt")
    ] = None,
    provider: Annotated[
        str, typer.Option("--provider", help="LLM provider (openai, anthropic, ollama)")
    ] = "openai",
    model: Annotated[
        str, typer.Option("--model", "-m", help="LLM model name")
    ] = "gpt-4o-mini",
):
    """
    Create a new prompt with proper structure.

    Examples:
        # Using root --project flag
        prompting_workbench --project my_project create-prompt 01-01 greeting_assistant

        # Using --project option
        prompting_workbench create-prompt 01-01 greeting_assistant --project my_project

        # With custom model
        prompting_workbench --project my_project create-prompt 01-02 summarizer --provider openai --model gpt-4
    """
    global plugin  # noqa: F821

    # Get project from context if not provided
    context: dict = dict(ctx.obj or {})
    project_name = project

    if not project_name:
        # Try to get from context (--project flag at root level)
        ctx_project = context.get("project")
        if ctx_project and ctx_project != "NONE":
            # Extract project_id if it's a Project object
            if hasattr(ctx_project, "project_id"):
                project_name = ctx_project.project_id
            else:
                project_name = str(ctx_project)
        else:
            # No project specified, use single workspace mode (empty project_id)
            # This will create prompts directly in PMPT_WRKBNCH_PROJECTS_DIR/prompts/
            project_name = ""

    plugin.notify_status_update(
        key="create-prompt",
        status="running",
        text=f"Creating prompt: {prompt_id}--{name}",
    )

    try:
        generator = BoilerplateGenerator(settings.projects_dir)
        prompt_path = generator.create_prompt(
            project_name=project_name,
            prompt_id=prompt_id,
            prompt_name=name,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            llm_provider=provider,
            llm_model=model,
        )

        plugin.notify_status_update(
            key="create-prompt", status="done", text=f"Prompt created: {prompt_path}"
        )

        console.print()
        console.rule("[bold green]Prompt Created Successfully[/bold green]")
        console.print()
        if project_name:
            console.print(f"[green]✓[/green] Project: [bold]{project_name}[/bold]")
        else:
            console.print(
                "[green]✓[/green] Workspace: [bold]Single (no project)[/bold]"
            )
        console.print(f"[green]✓[/green] Prompt ID: [bold]{prompt_id}--{name}[/bold]")
        console.print(f"[green]✓[/green] Location: [bold]{prompt_path}[/bold]")
        console.print(
            f"[green]✓[/green] Provider: [bold]{provider}[/bold] / Model: [bold]{model}[/bold]"
        )
        console.print()
        console.print("[bold cyan]Next steps:[/bold cyan]")
        console.print("  1. Edit the prompt templates:")
        console.print(f"     [yellow]- {prompt_path}/llm_system.jinja2[/yellow]")
        console.print(f"     [yellow]- {prompt_path}/user_prompt.jinja2[/yellow]")
        console.print()
        console.print("  2. Update input files:")
        console.print(
            f"     [yellow]- {prompt_path}/prompt_inputs/default/user_input.md[/yellow]"
        )
        console.print(
            f"     [yellow]- {prompt_path}/system_inputs/default/system_instructions.md[/yellow]"
        )
        console.print()

    except ValueError as e:
        plugin.notify_status_update(key="create-prompt", status="error", text=str(e))
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)
