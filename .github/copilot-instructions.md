# GitHub Copilot Instructions for Prompting Workbench

## Project Overview
This is a modular command-line workbench for developing, running, organizing, and evaluating Generative AI prompts across multiple LLMs. Built with Python 3.11+, focusing on reproducibility, structured experimentation, extensibility, and automation in prompt engineering workflows.

## Code Style & Standards

### Python Version & Typing
- Use Python 3.11+ features
- Always include type hints for function parameters and return types
- Use `from typing import` for generic types (List, Dict, Optional, etc.)
- Use `typing_extensions.Annotated` for enhanced type hints
- Prefer explicit typing over implicit

### Code Organization
- Keep functions small and focused on a single responsibility
- Use explicit, descriptive naming over abbreviated or "magic" names
- Avoid introducing heavy dependencies without discussion
- Follow domain-driven design patterns (domains, models, repositories)

### Formatting & Linting
- Use Ruff for linting and formatting
- Follow double-quote style for strings (configured in pyproject.toml)
- Ruff configuration: select = ["E4", "E7", "E9", "F", "Q"]
- Per-file ignores: E402 for __init__.py and test files
- Exclude .venv from linting

### Dependencies & Package Management
- Use `uv` for dependency management (preferred)
- Workspace structure: monorepo with packages in `packages/`
- Main package: `prompting-workbench` (workspace member)
- Dev dependencies: pytest, ruff

### Project Structure Conventions

#### Environment Variables
- ALL environment variables MUST use prefix: `PMPT_WRKBNCH_`
- Example: `PMPT_WRKBNCH_PROJECTS_DIR`
- Load from `.env` and `.env.wrkbnch` files automatically at startup

#### Project & Prompt Naming
- Prompt folders follow pattern: `NN-NN--slug` (e.g., `01-01--greeting_prompt`)
- Projects stored in: `wrkbnch_projects_space/`
- Standard prompt structure:
  ```
  prompts/
    <prompt_id>/
      llm_system.jinja2
      user_prompt.jinja2
      prompt_inputs/default/
      system_inputs/default/
      eval/
  ```

### Model & Domain Classes
- All models inherit from `ModelBase` (Pydantic BaseModel)
- Use Pydantic validators and serializers with `Annotated` types
- Example pattern:
  ```python
  from pydantic import PlainValidator, PlainSerializer
  from typing import Annotated
  
  field: Annotated[
      CustomType,
      PlainValidator(validator_func),
      PlainSerializer(serializer_func, return_type),
  ]
  ```

### Repository Pattern
- All repositories inherit from appropriate base classes:
  - `FileSystemRepositoryBase` for file-based operations
  - `MetaConfigRepositoryBase` for config management
- Repository methods should handle path resolution and validation
- Raise descriptive `ValueError` for missing resources

### Plugin System
- Plugins inherit from `BaseCliPlugin`
- Each plugin requires:
  - Main plugin class (e.g., `runner.py`)
  - CLI module (e.g., `runner_cli.py`) with `typer_app` object
- Plugin methods to implement:
  - `get_plugin_name()` - returns plugin identifier
  - `get_plugin_description()` - returns description
  - `get_plugin_help()` - returns help text
  - `get_plugin_file_path()` - returns `__file__`
  - `prepare()` - initialization logic
  - `run()` - main execution logic
- Use signal pattern (`blinker`) for status updates:
  ```python
  self.notify_status_update(key="operation", status="running", text="Description")
  ```

### CLI Development (Typer)
- Use Typer for CLI interface
- Use `Annotated` for option/argument definitions
- Include rich help text and metavar for clarity
- Support flags: `--debug`, `--dry-run`, `--project`, `-P` (prompts)
- Context passed via `ctx.obj` dictionary

### Console Output (Rich)
- Use Rich Console for formatted output
- Status indicators:
  - `[yellow]running[/yellow]`
  - `[green]done[/green]`
- Plugin output format: `[timestamp][plugin_name][key][status] message`
- Use `console.rule()` for section separators

### Comments
- Only comment code that needs clarification
- Avoid obvious or redundant comments
- Prefer self-documenting code through naming

### Testing
- Use pytest for testing
- Run tests with: `make test` or `uv run pytest`
- Tests not mandatory for every change but recommended

### Documentation
- Keep README.md updated for significant features
- Use docstrings for classes and complex functions
- Follow existing documentation patterns

## Common Patterns

### Dynamic Module Loading
```python
import importlib
spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
```

### Path Resolution
```python
import os
path = os.path.join(base_dir, sub_dir, file)
if not os.path.isdir(path):
    raise ValueError(f"Directory {path} does not exist")
```

### Environment Setup
```python
import dotenv
dotenv.load_dotenv(".env", override=True)
```

## Build & Run Commands
- Install: `make install` or `uv sync --dev`
- Run CLI: `make run ARGS="--project my_project"`
- Lint: `make lint` (ruff check)
- Format: `make format` (ruff format)
- Fix lint: `make lint-fix` (ruff check --fix)
- Test: `make test` (pytest)
- Clean: `make clean`

## Architecture Principles
- Plugin-based architecture for extensibility
- Domain-driven design for business logic
- Repository pattern for data access
- Dependency injection for testability
- Signal/event pattern for cross-cutting concerns

## What NOT to Do
- Do NOT introduce magic numbers or obscure abbreviations
- Do NOT add heavy dependencies without discussion
- Do NOT skip type hints
- Do NOT use single quotes for strings (use double quotes)
- Do NOT modify working code without good reason
- Do NOT hardcode paths; use config/environment variables with `PMPT_WRKBNCH_` prefix
