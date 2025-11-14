import os
from typing import Dict, Optional


class BoilerplateGenerator:
    """
    Handles generation of boilerplate structures for projects and prompts.
    """

    def __init__(self, projects_dir: str):
        self.projects_dir = projects_dir

    def validate_prompt_id(self, prompt_id: str) -> bool:
        """
        Validate prompt ID format (NN-NN).
        """
        import re
        pattern = r"^[0-9]{2}-[0-9]{2}$"
        return bool(re.match(pattern, prompt_id))

    def project_exists(self, project_name: str) -> bool:
        """
        Check if a project already exists.
        For empty project_name (single workspace mode), always returns True.
        """
        if not project_name:
            # Single workspace mode - prompts go directly in projects_dir/prompts/
            return True
        
        project_path = os.path.join(self.projects_dir, project_name)
        return os.path.isdir(project_path)

    def prompt_exists(self, project_name: str, prompt_id: str, prompt_name: str) -> bool:
        """
        Check if a prompt already exists.
        """
        if not project_name:
            # Single workspace mode
            prompt_dir = os.path.join(self.projects_dir, "prompts", f"{prompt_id}--{prompt_name}")
        else:
            prompt_dir = os.path.join(
                self.projects_dir,
                project_name,
                "prompts",
                f"{prompt_id}--{prompt_name}"
            )
        return os.path.isdir(prompt_dir)

    def create_project(self, project_name: str, description: str = "Project description") -> str:
        """
        Create a new project with proper structure.
        Returns the path to the created project.
        """
        project_path = os.path.join(self.projects_dir, project_name)

        if self.project_exists(project_name):
            raise ValueError(f"Project already exists: {project_name}")

        os.makedirs(os.path.join(project_path, "prompts"), exist_ok=True)
        os.makedirs(os.path.join(project_path, ".config"), exist_ok=True)

        meta_info = {
            "name": project_name,
            "description": description,
            "version": "0.1.0",
            "defaults": {
                "prompt": {}
            }
        }

        self._write_json(
            os.path.join(project_path, ".config", "meta_info.json"),
            meta_info
        )

        readme_content = f"""# {project_name}

{description}

## Prompts

This project contains the following prompts:

- (Add your prompts here)

## Usage

```bash
# Run all prompts in this project
prompting_workbench --project {project_name}

# Run specific prompt
prompting_workbench --project {project_name} -P <prompt_id>
```

## Configuration

- Project config: `.config/meta_info.json`
- Prompts location: `prompts/`
"""

        self._write_file(os.path.join(project_path, "README.md"), readme_content)

        return project_path

    def create_prompt(
        self,
        project_name: str,
        prompt_id: str,
        prompt_name: str,
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o-mini"
    ) -> str:
        """
        Create a new prompt with proper structure.
        Returns the path to the created prompt.
        
        If project_name is empty, creates prompt in single workspace mode
        (directly under projects_dir/prompts/).
        """
        if not self.validate_prompt_id(prompt_id):
            raise ValueError("Invalid prompt_id format. Must be NN-NN (e.g., 01-03)")

        if not self.project_exists(project_name):
            raise ValueError(f"Project does not exist: {project_name}")

        if self.prompt_exists(project_name, prompt_id, prompt_name):
            raise ValueError(f"Prompt already exists: {prompt_id}--{prompt_name}")

        # Determine prompt directory based on workspace mode
        if not project_name:
            # Single workspace mode - prompts go directly under projects_dir/prompts/
            prompt_dir = os.path.join(self.projects_dir, "prompts", f"{prompt_id}--{prompt_name}")
        else:
            # Multi-project mode
            prompt_dir = os.path.join(
                self.projects_dir,
                project_name,
                "prompts",
                f"{prompt_id}--{prompt_name}"
            )

        os.makedirs(os.path.join(prompt_dir, "prompt_inputs", "default"), exist_ok=True)
        os.makedirs(os.path.join(prompt_dir, "system_inputs", "default"), exist_ok=True)
        os.makedirs(os.path.join(prompt_dir, "eval"), exist_ok=True)
        os.makedirs(os.path.join(prompt_dir, ".config", "runner"), exist_ok=True)

        system_prompt_content = system_prompt or """You are a helpful AI assistant.

{{ system_instructions }}"""

        user_prompt_content = user_prompt or """{{ user_input }}

Please provide a detailed and helpful response."""

        self._write_file(
            os.path.join(prompt_dir, "llm_system.jinja2"),
            system_prompt_content
        )

        self._write_file(
            os.path.join(prompt_dir, "user_prompt.jinja2"),
            user_prompt_content
        )

        self._write_file(
            os.path.join(prompt_dir, "prompt_inputs", "default", "user_input.md"),
            "Write your user input here.\n\nYou can use multiple lines and markdown formatting.\n"
        )

        self._write_file(
            os.path.join(prompt_dir, "system_inputs", "default", "system_instructions.md"),
            "Follow these guidelines:\n- Be helpful and accurate\n- Provide clear explanations\n- Use examples when appropriate\n"
        )

        meta_info = {
            "system": '<file src="llm_system.jinja2"/>',
            "system_input": {
                "system_instructions": '<file src="system_inputs/default/system_instructions.md"/>'
            },
            "prompt": '<file src="user_prompt.jinja2"/>',
            "prompt_input": {
                "user_input": '<file src="prompt_inputs/default/user_input.md"/>'
            }
        }

        self._write_json(
            os.path.join(prompt_dir, ".config", "meta_info.json"),
            meta_info
        )

        execution_plan = {
            "llm_providers": [
                {
                    "provider": llm_provider,
                    "model": llm_model
                }
            ]
        }

        self._write_json(
            os.path.join(prompt_dir, ".config", "runner", "execution_plan.json"),
            execution_plan
        )

        test_config = {
            "enabled": True,
            "scenarios": [
                "scenario-001-basic.test.md"
            ]
        }

        self._write_json(
            os.path.join(prompt_dir, "eval", "test_config.json"),
            test_config
        )

        test_scenario = """# Test Scenario: Basic Functionality

## Expected Behavior
- Should respond appropriately to user input
- Should follow system instructions
- Should maintain helpful and professional tone

## Test Cases
1. Basic greeting
2. Complex question
3. Request for clarification
"""

        self._write_file(
            os.path.join(prompt_dir, "eval", "scenario-001-basic.test.md"),
            test_scenario
        )

        return prompt_dir

    def _write_file(self, file_path: str, content: str):
        """Write content to a file."""
        with open(file_path, "w") as f:
            f.write(content)

    def _write_json(self, file_path: str, data: Dict):
        """Write JSON data to a file."""
        import json
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
