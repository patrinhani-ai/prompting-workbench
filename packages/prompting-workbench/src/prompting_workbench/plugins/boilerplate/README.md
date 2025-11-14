# Boilerplate Plugin

The **boilerplate** plugin helps you quickly generate project and prompt structures with all the necessary files and directories.

## Commands

### create-project

Create a new project with proper directory structure.

**Usage:**
```bash
prompting_workbench create-project <name> [OPTIONS]
```

**Arguments:**
- `name` - Project name (required)

**Options:**
- `--description`, `-d` - Project description (default: "Project description")

**Example:**
```bash
prompting_workbench create-project my_ai_project --description "AI project for text summarization"
```

**Creates:**
```
wrkbnch_space/my_ai_project/
├── prompts/                    # Directory for prompts
├── .config/
│   └── meta_info.json         # Project configuration
└── README.md                   # Project documentation
```

---

### create-prompt

Create a new prompt within an existing project.

**Usage:**
```bash
prompting_workbench create-prompt <project> <prompt_id> <name> [OPTIONS]
```

**Arguments:**
- `project` - Project name (must exist)
- `prompt_id` - Prompt ID in format `NN-NN` (e.g., `01-01`, `02-05`)
- `name` - Descriptive prompt name (e.g., `greeting_assistant`)

**Options:**
- `--system`, `-s` - Custom system prompt text
- `--user`, `-u` - Custom user prompt text
- `--provider`, `-p` - LLM provider (default: `openai`)
- `--model`, `-m` - LLM model name (default: `gpt-4o-mini`)

**Examples:**
```bash
# Basic prompt creation
prompting_workbench create-prompt my_project 01-01 greeting_assistant

# With custom LLM model
prompting_workbench create-prompt my_project 01-02 summarizer --provider openai --model gpt-4

# With custom prompts
prompting_workbench create-prompt my_project 01-03 analyzer \
  --system "You are a data analyst" \
  --user "Analyze the following data: {{ data }}"
```

**Creates:**
```
prompts/01-01--greeting_assistant/
├── llm_system.jinja2              # System prompt template
├── user_prompt.jinja2             # User prompt template
├── prompt_inputs/
│   └── default/
│       └── user_input.md          # User input variables
├── system_inputs/
│   └── default/
│       └── system_instructions.md # System input variables
├── eval/
│   ├── test_config.json           # Test configuration
│   └── scenario-001-basic.test.md # Basic test scenario
└── .config/
    ├── meta_info.json             # Prompt metadata
    └── runner/
        └── execution_plan.json    # LLM execution config
```

---

### list

List available templates and LLM providers.

**Usage:**
```bash
prompting_workbench list
```

**Example:**
```bash
prompting_workbench list
```

---

## Prompt Naming Convention

Prompts follow the pattern: `NN-NN--descriptive_name`

- **First NN**: Category/section number (01-99)
- **Second NN**: Sequence within category (01-99)
- **descriptive_name**: Lowercase slug with underscores or hyphens

**Examples:**
- `01-01--greeting_assistant` - First prompt in category 1
- `02-03--data_analyzer` - Third prompt in category 2
- `05-01--code_reviewer` - First prompt in category 5

**Benefits:**
- Natural sorting by ID
- Easy categorization
- Self-documenting names

---

## Supported LLM Providers

### OpenAI
```bash
--provider openai --model gpt-4
--provider openai --model gpt-4o-mini
--provider openai --model gpt-3.5-turbo
```

### Anthropic
```bash
--provider anthropic --model claude-3-opus-20240229
--provider anthropic --model claude-3-sonnet-20240229
```

### Ollama (Local)
```bash
--provider ollama --model llama2
--provider ollama --model mistral
```

---

## Quick Start Workflow

### 1. Create a new project
```bash
prompting_workbench create-project my_ai_project
```

### 2. Create your first prompt
```bash
prompting_workbench create-prompt my_ai_project 01-01 summarizer
```

### 3. Edit the templates
```bash
# Edit system prompt
nano wrkbnch_space/my_ai_project/prompts/01-01--summarizer/llm_system.jinja2

# Edit user prompt
nano wrkbnch_space/my_ai_project/prompts/01-01--summarizer/user_prompt.jinja2
```

### 4. Edit input files
```bash
# Edit user input
nano wrkbnch_space/my_ai_project/prompts/01-01--summarizer/prompt_inputs/default/user_input.md

# Edit system instructions
nano wrkbnch_space/my_ai_project/prompts/01-01--summarizer/system_inputs/default/system_instructions.md
```

---

## Tips & Best Practices

### Multiple Input Variants

Create different input variants for testing:

```bash
# Create variant directory
mkdir -p wrkbnch_space/my_project/prompts/01-01--summarizer/prompt_inputs/variant_long_text

# Add custom input
echo "Long text to summarize..." > wrkbnch_space/my_project/prompts/01-01--summarizer/prompt_inputs/variant_long_text/user_input.md
```

### Organize Prompts by Category

Use the first number in the prompt ID to organize by category:

- `01-XX` - Text generation prompts
- `02-XX` - Data analysis prompts
- `03-XX` - Code generation prompts
- `04-XX` - Translation prompts
- `05-XX` - Question answering prompts

### Test Scenarios

Add comprehensive test scenarios in the `eval/` directory:

```bash
cat > wrkbnch_space/my_project/prompts/01-01--summarizer/eval/scenario-002-long-text.test.md << 'EOF'
# Test Scenario: Long Text Handling

## Description
Test how the prompt handles long documents

## Expected Behavior
- Should provide concise summary
- Should maintain key points
- Should stay within token limits
EOF
```

---

## Troubleshooting

### Invalid Prompt ID Format

**Error:** "Invalid prompt_id format. Must be NN-NN"

**Solution:** Use two-digit format with hyphen:
- ✅ Valid: `01-01`, `12-05`, `99-99`
- ❌ Invalid: `1-1`, `01-1`, `a1-01`

### Project Already Exists

**Error:** "Project already exists: my_project"

**Solution:** Choose a different name or delete the existing project:
```bash
rm -rf wrkbnch_space/my_project
```

### Prompt Already Exists

**Error:** "Prompt already exists: 01-01--my_prompt"

**Solution:** Use a different prompt ID or name:
```bash
prompting_workbench create-prompt my_project 01-02 my_prompt_v2
```
