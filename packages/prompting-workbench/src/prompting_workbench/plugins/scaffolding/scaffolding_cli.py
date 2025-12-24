import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from prompting_workbench.plugins.scaffolding.domains.scaffolding_generator import (
    ScaffoldingGenerator,
)
from prompting_workbench.plugins.scaffolding.scaffolding import ScaffoldingCliPlugin
from prompting_workbench.settings import settings

typer_app = typer.Typer(help="Scaffold new projects and prompts")
plugin: ScaffoldingCliPlugin  # noqa: F821  # Injected by CLI engine at runtime

console = Console()


@typer_app.command("scaffolding")
def scaffolding(
    ctx: typer.Context,
    list_templates: Annotated[
        bool,
        typer.Option(
            "--list-templates",
            help="List available templates and examples",
        ),
    ] = False,
    create_project: Annotated[
        str | None,
        typer.Option(
            "--create-project",
            help="Create a new project with the specified name",
            metavar="PROJECT_NAME",
        ),
    ] = None,
    create_prompt: Annotated[
        str | None,
        typer.Option(
            "--create-prompt",
            help="Create a new prompt (format: PROMPT_ID PROMPT_NAME, e.g., '01-01 my_prompt')",
            metavar="PROMPT_SPEC",
        ),
    ] = None,
    project: Annotated[
        str | None,
        typer.Option(
            "--project",
            "-p",
            help="Project name (for --create-prompt, optional if using root --project flag)",
        ),
    ] = None,
    description: Annotated[
        str,
        typer.Option(
            "--description",
            "-d",
            help="Project description (for --create-project)",
        ),
    ] = "Project description",
    system_prompt: Annotated[
        str | None,
        typer.Option(
            "--system",
            "-s",
            help="Custom system prompt (for --create-prompt)",
        ),
    ] = None,
    user_prompt: Annotated[
        str | None,
        typer.Option(
            "--user",
            "-u",
            help="Custom user prompt (for --create-prompt)",
        ),
    ] = None,
    provider: Annotated[
        str,
        typer.Option(
            "--provider",
            help="LLM provider (for --create-prompt: openai, anthropic, ollama)",
        ),
    ] = "openai",
    model: Annotated[
        str,
        typer.Option(
            "--model",
            "-m",
            help="LLM model name (for --create-prompt)",
        ),
    ] = "gpt-4o-mini",
):
    """
    Scaffold new projects and prompts with proper structure.

    Examples:
        # List available templates
        prompting-workbench scaffolding --list-templates

        # Create a new project
        prompting-workbench scaffolding --create-project my_new_project

        # Create a new prompt in the default project
        prompting-workbench scaffolding --create-prompt "01-01 my_prompt"

        # Create a prompt with specific project
        prompting-workbench scaffolding --create-prompt "01-02 greeting" --project my_project

        # Create prompt with custom model
        prompting-workbench scaffolding --create-prompt "01-03 summarizer" --provider openai --model gpt-4
    """
    global plugin  # noqa: F821

    # Get context from parent command
    context: dict = dict(ctx.obj or {})

    # Ensure plugin is prepared with context
    plugin.prepare(context=context)

    # Determine which action to perform
    if list_templates:
        _list_templates()
    elif create_project:
        _create_project(context, create_project, description)
    elif create_prompt:
        _create_prompt(
            context,
            create_prompt,
            project,
            system_prompt,
            user_prompt,
            provider,
            model,
        )
    else:
        # No action specified, show help
        console.print(
            "[yellow]No action specified. Use --help to see available options.[/yellow]"
        )
        console.print()
        console.print("Quick examples:")
        console.print("  • List templates: [cyan]--list-templates[/cyan]")
        console.print("  • Create project: [cyan]--create-project my_project[/cyan]")
        console.print(
            "  • Create prompt:  [cyan]--create-prompt '01-01 my_prompt'[/cyan]"
        )
        console.print()


def _list_templates():
    """List available templates and examples."""
    console.print()
    console.rule("[bold cyan]Available Templates[/bold cyan]")
    console.print()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Example", style="yellow")

    table.add_row(
        "Project",
        "Basic project structure",
        "scaffolding --create-project my_project",
    )
    table.add_row(
        "Prompt",
        "Basic prompt with system/user templates",
        "scaffolding --create-prompt '01-01 my_prompt'",
    )

    console.print(table)
    console.print()

    console.print("[bold cyan]LLM Providers:[/bold cyan]")
    console.print("  • openai    - OpenAI models (gpt-4, gpt-4o-mini, etc.)")
    console.print("  • anthropic - Anthropic models (claude-3-opus, etc.)")
    console.print("  • ollama    - Local models via Ollama")
    console.print()


def _create_project(context: dict, name: str, description: str):
    """Create a new project with proper structure."""
    plugin.notify_status_update(
        key="create-project", status="running", text=f"Creating project: {name}"
    )

    try:
        generator = ScaffoldingGenerator(settings.projects_dir)
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
            f"     [yellow]prompting-workbench scaffolding --create-prompt '01-01 my_first_prompt' --project {name}[/yellow]"
        )
        console.print()

    except ValueError as e:
        plugin.notify_status_update(key="create-project", status="error", text=str(e))
        console.print(f"[red]✗ Error:[/red] {e}")
        raise typer.Exit(code=1)


def _create_prompt(
    context: dict,
    prompt_spec: str,
    project: str | None,
    system_prompt: str | None,
    user_prompt: str | None,
    provider: str,
    model: str,
):
    """Create a new prompt with proper structure."""
    # Parse prompt_spec (format: "prompt_id prompt_name" or "prompt_id--prompt_name")
    parts = prompt_spec.strip().split(None, 1)
    if len(parts) != 2:
        console.print(
            "[red]✗ Error:[/red] Invalid prompt specification. Expected format: 'PROMPT_ID PROMPT_NAME'"
        )
        console.print("  Example: '01-01 my_prompt'")
        raise typer.Exit(code=1)

    prompt_id, prompt_name = parts

    # Get project from context if not provided
    project_name: str = project if project else ""

    if not project_name:
        # Try to get from context (--project flag at root level)
        ctx_project = context.get("project")
        if ctx_project and ctx_project != "NONE":
            # Extract project_id if it's a Project object
            if hasattr(ctx_project, "project_id"):
                project_name = ctx_project.project_id
            else:
                project_name = str(ctx_project)
        # else: project_name remains "" for single workspace mode

    plugin.notify_status_update(
        key="create-prompt",
        status="running",
        text=f"Creating prompt: {prompt_id}--{prompt_name}",
    )

    try:
        generator = ScaffoldingGenerator(settings.projects_dir)
        prompt_path = generator.create_prompt(
            project_name=project_name,
            prompt_id=prompt_id,
            prompt_name=prompt_name,
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
        console.print(
            f"[green]✓[/green] Prompt ID: [bold]{prompt_id}--{prompt_name}[/bold]"
        )
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
