# Prompting Workbench (WIP)

A modular command-line workbench for developing, running, organizing, and evaluating Generative AI prompts across multiple Large Language Models (LLMs) and providers. Built for practitioners who want **reproducibility**, **structured experimentation**, **extensibility**, and **automation** in their prompt engineering workflows.

> Status: Early development (v0.1.0). Interfaces may change. Feedback and contributions are welcome!

---

## 🚀 Key Features

- **Unified CLI** to manage prompt projects and run prompts in structured workspaces.
- **Project & Prompt Organization**: Opinionated folder layout for portability and reproducibility.
- **Multi-Model Ready**: Designed to integrate with multiple LLM providers (OpenAI, Anthropic, etc.) via a pluggable engine (LangChain compatibility planned/ongoing).
- **Plugin Architecture**: Drop-in plugins with their own CLI commands via dynamic discovery.
- **Environment-Aware**: Uses `.env` and `.env.wrkbnch` files + namespaced variables (`PMPT_WRKBNCH_*`).
- **Evaluation Harness**: Co-locate test inputs, scenarios, and output expectations alongside each prompt.
- **Dry-Run & Debug Modes**: Safer iteration while designing and diagnosing prompt executions.
- **Typed Core**: Built with Pydantic for config & model validation.

---

## 📦 Installation

### Prerequisites

- Python >= 3.11
- (Optional) [uv](https://github.com/astral-sh/uv) for fast dependency management

### Using pip

```bash
pip install prompting-workbench
```

### Using uv (recommended for workspace dev)

```bash
uv pip install prompting-workbench
```

### From Source (Editable)

```bash
git clone https://github.com/patrinhani-ai/prompting-workbench.git
cd prompting-workbench
uv pip install -e .  # or: pip install -e .
```

Once installed, the CLI entrypoint is available as:

```bash
prompting_workbench --help
```

---

## 🧠 Concepts

| Concept | Description |
|---------|-------------|
| Project | A container grouping related prompts (e.g., a product feature, research line, or domain). |
| Prompt  | A unit of execution containing a `llm_system.jinja2` + `user_prompt.jinja2` template, plus inputs. |
| Scenario / Eval | Structured test cases for a prompt stored under its `eval/` folder. |
| Plugin  | An extension that can add commands / behaviors to the core CLI. |
| Workspace | The root directory where projects, prompts, and artifacts live. |

---

## 🗂️ Project & Prompt Layout

A typical prompt location inside a project:

```text
wrkbnch_projects_space/
  <project_name>/
    prompts/
      01-01--sample_prompt_01/
        llm_system.jinja2
        user_prompt.jinja2
        prompt_inputs/
          default/            # Input variable sets
        system_inputs/
          default/            # System-level inputs / context
        eval/
          input.test.md
          scenario-001-format.test.md
          scenario-002-security.test.md
          scenario-003-style.test.md
          scenario-004-content.test.md
          test_config.json
          test_output_template.json
```

Multiple projects can co-exist; samples may also be in `wrkbnch_sample_01/` or `wrkbnch_space/` depending on your setup.

---

## ⚙️ Environment Variables

All variables consumed by the tool are namespaced with the prefix `PMPT_WRKBNCH_`.

Core variables:

- `PMPT_WRKBNCH_PROJECTS_DIR` (default: `./wrkbnch_projects`): Root directory where project folders live.

Automatically loaded (if present):

- `.env`
- `.env.wrkbnch`

These are loaded at startup (see `setup()` in `cli.py`). Use them to store provider keys, model defaults, etc.

---

## 🧩 Plugin System

The CLI dynamically loads plugins by:

1. Discovering registered plugin objects in the engine (`cli_engine.plugins`).
2. Locating a sibling `<plugin_name>_cli.py` file.
3. Importing it dynamically and mounting its `typer_app` into the root CLI.
4. Attaching a status listener for rich, timestamped progress output.

Each plugin can:

- Expose additional subcommands.
- Emit status events (`running` → `done`).
- Extend evaluation, generation, or orchestration behaviors.

> To create a plugin, implement a subclass of `BaseCliPlugin`, ensure it is discoverable by `CliEngine`, and provide a `<plugin>_cli.py` that defines a `typer_app` object.

---

## 🏁 Quick Start

Initialize your workspace structure:

```bash
mkdir -p wrkbnch_projects_space/my_first_project/prompts
```

Create a prompt folder (follow naming pattern `NN-NN--slug` for ordering):

```bash
mkdir -p wrkbnch_projects_space/my_first_project/prompts/01-01--greeting_prompt/{prompt_inputs/default,system_inputs/default,eval}
```
Add templates:

```bash
$EDITOR wrkbnch_projects_space/my_first_project/prompts/01-01--greeting_prompt/llm_system.jinja2
$EDITOR wrkbnch_projects_space/my_first_project/prompts/01-01--greeting_prompt/user_prompt.jinja2
```
Run the CLI targeting your project:

```bash
prompting_workbench --project my_first_project
```
List project help (after plugin load):

```bash
prompting_workbench --project my_first_project --help
```

Run with debug / dry-run modes:

```bash
prompting_workbench --project my_first_project --debug --dry-run
```

Select only specific prompts (IDs correspond to folder names):

```bash
prompting_workbench --project my_first_project -P 01-01--greeting_prompt
```

> When `--project` is omitted (or `NONE`), the engine may operate in single / ad-hoc mode (implementation-dependent).

---

## 🧪 Evaluation Workflow

Each prompt's `eval/` directory may contain:

- `*.test.md` scenario files (format, style, security, content, etc.).
- `input.test.md` base or reference input.
- `test_config.json` orchestration and assertion config.
- `test_output_template.json` expected output structure (JSON schema-like guidance).

Planned / Typical Evaluation Steps:

1. Load prompt templates + input variables.
2. Render prompt variants.
3. Execute against configured models/providers.
4. Collect outputs + metadata.
5. Compare against evaluation assertions (future: scoring, LLM-as-judge, heuristics).

---

## 🧪 Example `.env` (placeholder)

```dotenv
PMPT_WRKBNCH_PROJECTS_DIR=./wrkbnch_projects_space
OPENAI_API_KEY=sk-...           # (If using OpenAI via a plugin)
ANTHROPIC_API_KEY=...           # (If using Anthropic via a plugin)
```

---

## 🔌 Extending

Create `my_plugin.py`:

```python
from prompting_workbench.plugins._base_cli_plugin import BaseCliPlugin

class MyPlugin(BaseCliPlugin):
    def get_plugin_name(self):
        return "my_plugin"

    def prepare(self):
        # discovery / pre-flight logic
        pass
```

Create `my_plugin_cli.py` (same directory):

```python
import typer
from rich import print
from .my_plugin import MyPlugin

typer_app = typer.Typer(help="My Plugin Commands")
plugin: MyPlugin  # injected dynamically by core loader

@typer_app.command()
def hello():
    print(f"[green]Hello from {plugin.get_plugin_name()}![/green]")
```
Ensure the plugin instance gets registered inside the `CliEngine` (e.g., during `prepare()`). The core then loads and mounts it automatically.

---

## 🏗️ Development

Clone and install in editable mode:

```bash
git clone https://github.com/patrinhani-ai/prompting-workbench.git
cd prompting-workbench
uv pip install -e .[dev]  # or: pip install -e .[dev]
```

Run lint & format:

```bash
uv run lint
uv run format
```
(Or directly with `ruff` if installed globally.)

Run CLI from source root:

```bash
python -m prompting_workbench.cli --help
```

---

## 🤝 Contributing

Contributions are welcome! Suggested flow:

1. Open an issue to discuss a significant change.
2. Fork the repo and create a feature branch (`feat/your-feature`).
3. Add/update docs and (future) tests.
4. Run formatters & linters.
5. Submit a PR referencing the issue.

Coding Guidelines:

- Follow Python 3.11+ typing practices.
- Keep functions small & focused.
- Prefer explicit naming over magic.
- Avoid introducing heavy dependencies without discussion.

Potential Areas to Help:

- LangChain integration layer
- Additional provider plugins (Azure OpenAI, Claude, Gemini, Local models)
- Evaluation metrics / judge models
- Prompt diffing / versioning utilities
- Rich TUI mode

---

## 🗺️ Roadmap (Indicative)

- [ ] LangChain integration layer
- [ ] Built-in OpenAI / Anthropic plugins
- [ ] Evaluation runner + scoring hooks
- [ ] Prompt version history + diffs
- [ ] Export / report generation (Markdown / HTML)
- [ ] CI-ready regression suite
- [ ] Embedded vector store for retrieval-augmented contexts
- [ ] Web dashboard (stretch)

---

## ❓ FAQ (Early Draft)

**Q: Why another prompting tool?**  
A: This project focuses on a clean, pluggable CLI-first workflow emphasizing reproducibility and testability.

**Q: Does it run locally without API keys?**  
A: Yes; you can develop templates and dry-run rendering logic without calling providers.

**Q: How are prompts selected?**  
A: Use `--project` plus `-P <prompt_id>` arguments; omit `-P` to run all prompts in a project.

---

## 📄 License

Released under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgements

Inspired by existing prompt tooling ecosystems, experiment trackers, and the philosophy of treating prompts as versioned, testable assets.

---

## ⭐ Support

If this project helps you, consider starring the repository and opening issues with suggestions.

---

> "Build prompts like software, not throwaways."
