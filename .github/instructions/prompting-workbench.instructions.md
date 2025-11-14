---
applyTo: "packages/prompting-workbench/**"
---
# GitHub Copilot Instructions - Prompting Workbench Package

## Package Overview
This is the core package for the Prompting Workbench CLI tool - a modular command-line workbench for developing, running, organizing, and evaluating Generative AI prompts across multiple LLMs.

**Main Source Code Location**: `packages/prompting-workbench/src/prompting_workbench/`

All development work should focus on the `packages/prompting-workbench/` directory.

## Package Configuration

### Dependencies (from pyproject.toml)
```toml
[project]
name = "prompting-workbench"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "pydantic>=2.11.7",
    "pydantic-settings>=2.10.1",
    "python-dotenv>=1.1.1",
    "typer>=0.17.3",
    "blinker>=1.9.0",
    "requests>=2.32.5",
    "jinja2>=3.1.6",
    "langchain>=1.0.3",
    "langchain-openai>=1.0.1",
    "langchain-ollama>=1.0.0",
]

[project.scripts]
prompting_workbench = "prompting_workbench.cli:main"
```

## Source Code Structure

```
packages/prompting-workbench/src/prompting_workbench/
├── cli.py                      # Main CLI entry point with Typer
├── cli_engine.py               # Engine orchestration & plugin loading
├── cli_engine_types.py         # ICliEngine interface
├── config.py                   # Pydantic settings (PMPT_WRKBNCH_* vars)
├── wrkbnch_context.py          # Global context object
│
├── core/                       # Core infrastructure layer
│   ├── models/
│   │   ├── model_base.py       # Base Pydantic model
│   │   ├── types.py            # Custom types (ContentStrRenderer, etc.)
│   │   └── validators.py       # Pydantic validators
│   ├── repositories/
│   │   └── repository_base.py  # Base repository class
│   └── utils/
│       └── io.py               # File I/O utilities
│
├── domains/                    # Domain logic layer
│   ├── project.py              # Project domain class
│   ├── prompt.py               # Prompt domain class
│   ├── llm_runner.py           # LLM execution logic
│   ├── models/                 # Domain Pydantic models
│   │   ├── project.py          # ProjectModel
│   │   └── prompt.py           # PromptModel
│   └── repositories/           # Data access layer
│       ├── project_repository.py
│       ├── prompt_repository.py
│       └── _core/              # Repository infrastructure
│           ├── fs_repository_base.py
│           ├── meta_config_fs_repository.py
│           └── meta_config_repository_base.py
│
└── plugins/                    # Plugin system
    ├── _base_cli_plugin.py     # BaseCliPlugin abstract class
    └── runner/                 # Example: Runner plugin
        ├── runner.py           # RunnerCliPlugin implementation
        ├── runner_cli.py       # Typer CLI commands
        └── domains/            # Plugin-specific domain logic
            ├── runner_controller.py
            ├── runner_task.py
            ├── models/
            └── repositories/
```

## Code Style & Standards

### Python Version & Typing
- **Python 3.11+** required
- Always include type hints for parameters and return values
- Use `from typing import` for List, Dict, Optional, etc.
- Use `typing_extensions.Annotated` for enhanced type hints
- Use union syntax: `str | None` instead of `Optional[str]`

### Code Organization Principles
- **Keep functions small** - single responsibility
- **Explicit naming** - no abbreviations or "magic" names
- **Domain-driven design** - separate concerns into core/domains/plugins
- **Dependency injection** - pass dependencies explicitly
- **Avoid heavy dependencies** without discussion

### Formatting & Linting
- **Ruff** for all linting and formatting
- **Double quotes** for strings (not single quotes)
- Run `make lint` or `make format` from repository root

## Environment Variables

### Naming Convention
- **ALL** environment variables use prefix: `PMPT_WRKBNCH_`
- Example: `PMPT_WRKBNCH_PROJECTS_DIR`
- Defined in `config.py` using `pydantic-settings`

### Loading Mechanism
```python
# At CLI startup (cli.py)
import dotenv
dotenv.load_dotenv(".env", override=True)

# Via Pydantic Settings (config.py)
class PromptWorkbenchSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PMPT_WRKBNCH_",
        env_file=".env.wrkbnch",
    )
```

## What NOT to Do

- ❌ Do NOT use single quotes for strings (use double quotes)
- ❌ Do NOT skip type hints
- ❌ Do NOT introduce magic numbers or obscure variable names
- ❌ Do NOT add heavy dependencies without discussion
- ❌ Do NOT hardcode paths; use `settings` or pass as parameters
- ❌ Do NOT use environment variables without `PMPT_WRKBNCH_` prefix
- ❌ Do NOT create circular imports
- ❌ Do NOT put business logic in repositories (use domain classes)
- ❌ Do NOT put data access in domain classes (use repositories)
- ❌ Do NOT modify working code without good reason

## Development Workflow

1. **Make changes** in `packages/prompting-workbench/src/prompting_workbench/`
2. **Follow existing patterns** from similar files
3. **Use absolute imports** from package root
4. **Add type hints** to all new code
5. **Run linting** from repo root: `make lint`
6. **Run formatting** from repo root: `make format`
7. **Test locally** with `make run ARGS="..."`

---

# Common Patterns & Conventions - Prompting Workbench

## Import Organization

```python
# Standard library
import os
import sys
from typing import List, Optional

# Third-party
from pydantic import BaseModel
import typer

# Local - absolute imports from package root
from prompting_workbench.config import settings
from prompting_workbench.domains.project import Project
from prompting_workbench.core.utils.io import get_json_content
```

**Rules**:
- Group imports: standard library, third-party, local
- Use absolute imports from package root (`prompting_workbench.`)
- Never use relative imports outside of the same subpackage

## Error Handling

```python
# Descriptive ValueError for business logic errors
if not os.path.isdir(project_path):
    raise ValueError(f"Project {project_id} does not exist")

# ImportError for module loading
if spec is None:
    raise ImportError(f"Could not find module spec for {file_path}")
```

**Rules**:
- Use `ValueError` for business logic validation errors
- Use `ImportError` for module loading failures
- Always include descriptive error messages with context
- Let exceptions bubble unless you have a specific reason to catch

## Path Handling

```python
import os

# Always use os.path.join
path = os.path.join(base_dir, "prompts", prompt_id)

# Check existence before use
if not os.path.exists(path):
    raise ValueError(f"Path {path} does not exist")

# Use os.path.isdir and os.path.isfile for type checking
if os.path.isdir(path):
    # directory logic
elif os.path.isfile(path):
    # file logic
```

**Rules**:
- Always use `os.path.join` for path construction
- Check path existence with `os.path.exists`
- Validate path type with `os.path.isdir` or `os.path.isfile`
- Never hardcode path separators (`/` or `\`)

## Rich Console Output

```python
from rich.console import Console

console = Console()

# Rules and headers
console.rule("[ [bold cyan]Section Title[/bold cyan] ]")

# Status colors
console.print(f"[yellow]running[/yellow] Operation in progress")
console.print(f"[green]done[/green] Operation complete")

# Plugin output format
console.print(f"[{timestamp}][magenta]{plugin_name}[/magenta][royal_blue1]{key}[/royal_blue1][green]{status}[/green] {text}")
```

**Status Colors**:
- `[yellow]` - running/in-progress
- `[green]` - done/success
- `[red]` - error/failure
- `[magenta]` - plugin name
- `[royal_blue1]` - keys/identifiers
- `[cyan]` - headers/titles

## Comments & Documentation

### When to Comment
- **Only when needed** for clarification
- Complex algorithms or non-obvious logic
- Public API methods (brief docstring)
- Avoid obvious comments like `# Increment counter`

### Docstring Style
```python
def load_prompts(self, prompt_ids: list[str] = []):
    """
    Load prompts associated with the project.
    This method loads prompts from the project directory.
    """
```

**Rules**:
- Brief, descriptive docstrings for public methods
- No need for parameter/return documentation (use type hints)
- Prefer self-documenting code over excessive comments

## Type Hints Best Practices

```python
# Use union syntax (Python 3.11+)
def get_project(self, project_id: str) -> Project | None:
    pass

# Use Annotated for enhanced type information
from typing_extensions import Annotated

prompts: Annotated[
    List[str],
    typer.Option("--prompts", "-P", help="List of prompts"),
] = []

# Use Optional with defaults
system_input: Optional[dict] = {}

# Type complex return values
def get_all_prompts(self, project_id) -> list[PromptModel]:
    pass
```

## File Operations

```python
# Reading files
content = get_file_content(file_path)
data = get_json_content(json_path)

# Writing files
write_file(file_path, content)
write_json_file(json_path, data)

# Walking directories
for root, file_name in walk_dir_files(folder_path):
    file_path = os.path.join(root, file_name)
```

**Rules**:
- Use utility functions from `core/utils/io.py`
- Don't duplicate file I/O logic
- JSON files always use `indent=4`

## Dictionary Merging

```python
# Merge with unpacking
config = {"id": prompt_id, **defaults, **prompt_config}

# Get with defaults
context = kwargs.get("context", {})
```

## List Operations

```python
# Deduplicate with set
unique_prompts = list(set(prompts))

# Conditional population
prompt_ids = prompt_ids or self.prompts_repository.get_all_prompt_ids(project_id)

# Check emptiness
if not prompt_ids or len(prompt_ids) == 0:
    # load all
```

## String Formatting

```python
# Use f-strings (not .format() or %)
error_msg = f"Project {project_id} does not exist"
log_msg = f"[{timestamp}][{plugin_name}] {text}"

# Multi-line strings
help_text = """
Environment variables:
- PMPT_WRKBNCH_PROJECTS_DIR
"""
```

## Context Managers

```python
# Use 'with' for file operations (already done in utils)
with open(file_path) as f:
    content = f.read()

with open(file_path, "w") as f:
    f.write(content)
```

## Property Decorators

```python
class BaseCliPlugin:
    @property
    def project(self) -> Project | None:
        return self.context.project
```

**Rules**:
- Use `@property` for computed or delegated attributes
- Keep property getters simple (no complex logic)

## Static Methods

```python
class Project:
    @staticmethod
    def load(project_id: str):
        return Project(project_id)
```

**Rules**:
- Use `@staticmethod` for factory methods
- Common pattern: `load()`, `create()`, `from_*()` methods

## Abstract Methods

```python
from abc import abstractmethod

class BaseCliPlugin:
    @abstractmethod
    def get_plugin_name(self):
        return "no_name"

    @abstractmethod
    def run(self):
        pass
```

**Rules**:
- Use `@abstractmethod` for methods that must be implemented
- Provide sensible defaults or raise `NotImplementedError`

## Signal/Event Pattern (Blinker)

```python
from blinker import signal

class BaseCliPlugin:
    on_status_update = signal("on_status_update")

    def listen_on_status_update(self, handler):
        self.on_status_update.connect(handler)

    def notify_status_update(self, key: str, status: str = "", text: str = ""):
        self.on_status_update.send(self, key=key, status=status, text=text)
```

**Rules**:
- Use signals for cross-cutting concerns (logging, status updates)
- Signals defined as class attributes
- Use `send()` to emit, `connect()` to subscribe

## Example: Adding a New Plugin

1. **Create plugin directory**: `src/prompting_workbench/plugins/myplugin/`
2. **Create plugin class** (`myplugin.py`):
```python
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

class MyPlugin(BaseCliPlugin):
    def get_plugin_name(self):
        return "myplugin"

    def get_plugin_description(self):
        return "My plugin description"

    def get_plugin_help(self):
        return "My plugin help"

    def get_plugin_file_path(self):
        return __file__

    def prepare(self, *args, **kwargs):
        self.set_context(**kwargs.get("context", {}))

    def run(self):
        # Implementation
        pass
```

3. **Create CLI module** (`myplugin_cli.py`):
```python
import typer
from .myplugin import MyPlugin

typer_app = typer.Typer(help="My plugin commands")
plugin: MyPlugin

@typer_app.command()
def do_something():
    """Do something useful"""
    plugin.notify_status_update(key="task", status="running", text="Starting task")
    plugin.run()
    plugin.notify_status_update(key="task", status="done", text="Task complete")
```

4. **Register in cli_engine.py**:
```python
def _load_plugins(self):
    from prompting_workbench.plugins.myplugin.myplugin import MyPlugin
    self._load_plugin(MyPlugin())
```

---

# Architecture Patterns - Prompting Workbench

This file documents the key architectural patterns used in `packages/prompting-workbench/`.

## 1. Settings with Pydantic Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class PromptWorkbenchSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PMPT_WRKBNCH_",
        env_file=".env.wrkbnch",
        yaml_file=".wrkbnch.yaml",
        env_file_encoding="utf-8",
    )

    projects_dir: str = "./wrkbnch_space"

settings = PromptWorkbenchSettings()
```

**Rules**:
- ALL environment variables use `PMPT_WRKBNCH_` prefix
- Settings loaded from `.env.wrkbnch` and `.wrkbnch.yaml`
- Singleton instance exported as `settings`

## 2. Context Pattern

```python
from prompting_workbench.domains.project import Project

class WrkbnchContext:
    project: Project | None = None
    debug: bool = False
    dry_run: bool = False

    def __init__(self, project: Project | None = None, debug: bool = False, dry_run: bool = False):
        self.project = project
        self.debug = debug
        self.dry_run = dry_run
```

**Rules**:
- Global context shared across engine and plugins
- Holds current project, debug flags, etc.
- Passed to plugins during initialization

## 3. Domain Classes

```python
class Project:
    data: ProjectModel              # Pydantic model for validation
    repository: ProjectRepository   # Data access
    prompts_repository: PromptRepository

    project_id: str
    prompts: list[Prompt]

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.prompts = []
        self.repository = ProjectRepository()
        self.prompts_repository = PromptRepository()
        self._load()

    def _load(self):
        self.data = self.repository.get_project(self.project_id)

    @staticmethod
    def load(project_id: str):
        return Project(project_id)
```

**Rules**:
- Domain classes orchestrate business logic
- Use Pydantic models (`data` property) for validation
- Use repositories for data access
- Static `load()` factory method pattern
- Private `_load()` for initialization logic

## 4. Pydantic Models

```python
from typing import Annotated, Optional
from pydantic import PlainValidator, PlainSerializer
from prompting_workbench.core.models.model_base import ModelBase
from prompting_workbench.core.models.types import ContentStrRenderer

class PromptModel(ModelBase):
    id: str

    system: Annotated[
        ContentStrRenderer,
        PlainValidator(py_validator_content_str_renderer),
        PlainSerializer(lambda x: x.lazy_value, str),
    ] = ContentStrRenderer("")

    system_input: Optional[dict] = {}
    prompt: Annotated[ContentStrRenderer, ...] = ContentStrRenderer("")
    prompt_input: Optional[dict] = {}
```

**Rules**:
- Inherit from `ModelBase` (which extends Pydantic's `BaseModel`)
- Use `Annotated` for custom validators and serializers
- Use `Optional[dict]` with default `{}`
- Custom types go in `core/models/types.py`
- Validators go in `core/models/validators.py`

## 5. Repository Pattern

```python
from prompting_workbench.domains.repositories._core.fs_repository_base import FileSystemRepositoryBase

class PromptRepository(FileSystemRepositoryBase):
    def get_prompt_dir(self, project_id: str, prompt_id: str) -> str:
        return os.path.join(self.get_project_dir(project_id), "prompts", prompt_id)

    def get_prompt(self, project_id, prompt_id, defaults: dict = {}) -> PromptModel:
        project_path = self.get_project_dir(project_id)

        if not os.path.isdir(project_path):
            raise ValueError(f"Project {project_id} does not exist")

        prompt_path = os.path.join(project_path, "prompts", prompt_id)

        if not os.path.isdir(prompt_path):
            raise ValueError(f"Prompt {prompt_id} does not exist in project {project_id}")

        prompt_config = self.get_prompt_config(project_id, prompt_id)

        return PromptModel.model_validate(
            {"id": prompt_id, **defaults, **prompt_config},
            context={"base_path": prompt_path},
        )
```

**Rules**:
- Inherit from appropriate base: `FileSystemRepositoryBase`, `MetaConfigRepositoryBase`
- Handle path resolution with `os.path.join`
- Validate paths exist, raise `ValueError` with descriptive messages
- Return domain models, not raw data
- Use `defaults` parameter pattern for cascading config

## 6. Plugin System

```python
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin
from prompting_workbench.wrkbnch_context import WrkbnchContext

class RunnerCliPlugin(BaseCliPlugin):
    def get_plugin_name(self):
        return "runner"

    def get_plugin_description(self):
        return "Run prompts against LLM providers"

    def get_plugin_help(self):
        return "Execute prompts with configured models"

    def get_plugin_file_path(self):
        return __file__

    def prepare(self, *args, **kwargs):
        self.set_context(**kwargs.get("context", {}))
        # Plugin initialization

    def run(self):
        # Main execution logic
        pass
```

**Plugin CLI Module** (`runner_cli.py`):
```python
import typer
from rich import print
from .runner import RunnerCliPlugin

typer_app = typer.Typer(help="Runner plugin commands")
plugin: RunnerCliPlugin  # Injected by CLI engine

@typer_app.command()
def execute():
    """Execute prompts"""
    plugin.notify_status_update(key="execute", status="running", text="Starting execution")
    plugin.run()
    plugin.notify_status_update(key="execute", status="done", text="Execution complete")
```

**Rules**:
- Each plugin has two files: `<name>.py` and `<name>_cli.py`
- Inherit from `BaseCliPlugin`
- Implement all abstract methods
- Use `self.notify_status_update()` for progress reporting
- CLI module exports `typer_app` and receives `plugin` instance
- Use signals (`blinker`) for status updates

## 7. CLI with Typer

```python
import typer
from typing import List
from typing_extensions import Annotated
from rich.console import Console

typer_app = typer.Typer(no_args_is_help=True, help="CLI help text")
console = Console()

@typer_app.callback(invoke_without_command=True)
def typer_callback(
    ctx: typer.Context,
    project: Annotated[
        str,
        typer.Option(
            metavar="PROJECT_NAME",
            help="Prompt Project name to load in the CLI context",
        ),
    ] = "NONE",
    prompts: Annotated[
        List[str],
        typer.Option(
            "--prompts", "-P",
            metavar="PROMPT_ID",
            help="List of prompts to load",
        ),
    ] = [],
    debug: Annotated[bool, typer.Option("--debug", help="Enable debug mode")] = False,
):
    console.rule("[ [bold cyan]Prompt Workbench[/bold cyan] ]")
    ctx.obj = {"debug": debug, "project": project}
```

**Rules**:
- Use `Annotated` for all options/arguments
- Include `metavar` and `help` text
- Use Rich Console for formatted output
- Pass state via `ctx.obj` dictionary
- Support common flags: `--debug`, `--dry-run`, `--project`, `-P`

## 8. File I/O Utilities

```python
import json
import os

def get_file_content(file_path):
    with open(file_path) as f:
        return f.read()

def get_json_content(file_path):
    return json.load(open(file_path))

def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)

def write_json_file(file_path: str, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
```

**Rules**:
- All file utilities in `core/utils/io.py`
- Simple, focused functions
- No elaborate error handling (let exceptions bubble)
- Use `json.dump` with `indent=4` for readability

## 9. Dynamic Module Loading

```python
import importlib
import sys

def dynamic_import_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Could not find module spec for {file_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
```

**Rules**:
- Used for plugin CLI loading
- Add to `sys.modules` for standard import behavior
- Raise `ImportError` with clear message
