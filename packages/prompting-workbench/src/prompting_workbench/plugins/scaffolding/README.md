# Scaffolding Plugin

The Scaffolding plugin provides a unified command for generating boilerplate code and project structures in the Prompting Workbench.

## Overview

This plugin consolidates the functionality previously provided by separate boilerplate commands (`wb-list-templates`, `wb-create-project`, `wb-create-prompt`) into a single, unified `scaffolding` command with multiple options.

## Commands

### List Templates

List all available templates and examples:

```bash
prompting-workbench scaffolding --list-templates
```

### Create Project

Create a new project with proper directory structure:

```bash
prompting-workbench scaffolding --create-project PROJECT_NAME [--description DESCRIPTION]
```

**Options:**

- `--description, -d`: Project description (default: "Project description")

**Example:**

```bash
prompting-workbench scaffolding --create-project my_new_project --description "My awesome project"
```

### Create Prompt

Create a new prompt with system/user templates and configuration:

```bash
prompting-workbench scaffolding --create-prompt "PROMPT_ID PROMPT_NAME" [OPTIONS]
```

**Options:**

- `--project, -p`: Project name (optional if using root `--project` flag)
- `--system, -s`: Custom system prompt
- `--user, -u`: Custom user prompt
- `--provider`: LLM provider (openai, anthropic, ollama) [default: openai]
- `--model, -m`: LLM model name [default: gpt-4o-mini]

**Examples:**

```bash
# Create prompt in single workspace mode (no project)
prompting-workbench scaffolding --create-prompt "01-01 my_prompt"

# Create prompt in specific project
prompting-workbench scaffolding --create-prompt "01-01 greeting" --project my_project

# Create prompt with custom provider and model
prompting-workbench scaffolding --create-prompt "01-02 summarizer" --provider anthropic --model claude-3-opus
```

## Features

- **Unified Interface**: Single command for all scaffolding operations
- **Clear Help Text**: Comprehensive help and usage examples
- **Flexible Options**: Support for various LLM providers and models
- **Project Structure**: Automatically creates proper directory structure with:
  - Template files (`llm_system.jinja2`, `user_prompt.jinja2`)
  - Input directories (`prompt_inputs/default/`, `system_inputs/default/`)
  - Configuration files (`.config/meta_info.json`, `execution_plan.json`)

## Plugin Architecture

The scaffolding plugin follows the standard plugin pattern:

- **Plugin Class**: `ScaffoldingCliPlugin` (inherits from `BaseCliPlugin`)
- **CLI Module**: `scaffolding_cli.py` with `typer_app` object
- **Domain Logic**: `ScaffoldingGenerator` for project and prompt generation

## Dependencies

This plugin depends on:

- `prompting_workbench.plugins.scaffolding.domains.scaffolding_generator.ScaffoldingGenerator`
- `prompting_workbench.settings`
- `typer` for CLI interface
- `rich` for formatted console output
