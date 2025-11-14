# GitHub Copilot Integration Guide

## Overview

Skill Seekers now supports generating **GitHub Copilot knowledge bases** in addition to Claude AI skills. This guide explains how to use Skill Seekers to create Copilot-optimized documentation.

## What's the Difference?

### Claude AI Skills
- **Format:** `.zip` packages uploaded to Claude
- **Usage:** Natural language queries to Claude AI
- **Storage:** Claude's knowledge base
- **Best for:** Interactive AI assistance

### GitHub Copilot Knowledge Bases
- **Format:** `.github/copilot-instructions.md` + documentation files
- **Usage:** Code completion and inline suggestions
- **Storage:** Your repository
- **Best for:** Development-time code assistance

## How GitHub Copilot Works

GitHub Copilot uses several sources for context:
1. **`.github/copilot-instructions.md`** - Project-wide instructions (PRIMARY)
2. **Open files** - Currently visible code
3. **Repository structure** - File organization and naming
4. **Code comments** - Inline documentation
5. **Docstrings** - Function and class documentation

Skill Seekers focuses on generating optimized `.github/copilot-instructions.md` files and supporting documentation.

## Quick Start

### Step 1: Scrape Documentation

First, scrape the documentation as usual:

```bash
# Using a preset config
skill-seekers scrape --config configs/react.json

# Or create your own
skill-seekers scrape --url https://react.dev/ --name react --description "React framework"
```

This creates `output/react_data/` with scraped content.

### Step 2: Generate Copilot Knowledge Base

Convert the scraped data to Copilot format:

```bash
skill-seekers copilot --config configs/react.json --data-dir output/react_data/
```

This creates `output/react_copilot/` with:
```
react_copilot/
├── .github/
│   ├── copilot-instructions.md   # Main instruction file
│   └── copilot-config.json       # Configuration metadata
├── docs/
│   ├── code-patterns.md          # Common patterns
│   └── api-reference.md          # API documentation
├── examples/
│   ├── javascript-examples.md    # JS code examples
│   └── typescript-examples.md    # TS code examples
└── README.md                      # Usage instructions
```

### Step 3: Use in Your Project

Copy the Copilot instructions to your project:

```bash
# Option 1: Copy to existing project
cp output/react_copilot/.github/copilot-instructions.md your-project/.github/

# Option 2: Copy entire directory
cp -r output/react_copilot/.github your-project/
cp -r output/react_copilot/docs your-project/docs/copilot/
```

### Step 4: Start Coding

GitHub Copilot will automatically:
- Read `.github/copilot-instructions.md`
- Provide context-aware suggestions
- Use the documented patterns and APIs
- Offer better code completions

## Complete Workflow

### For React

```bash
# 1. Scrape React docs
skill-seekers scrape --config configs/react.json

# 2. Generate Copilot knowledge base
skill-seekers copilot --config configs/react.json --data-dir output/react_data/

# 3. Copy to your React project
cp output/react_copilot/.github/copilot-instructions.md ~/my-react-app/.github/

# 4. Start coding with improved Copilot suggestions!
cd ~/my-react-app
code .  # Copilot will use the new instructions
```

### For Django

```bash
# 1. Scrape Django docs
skill-seekers scrape --config configs/django.json

# 2. Generate Copilot knowledge base
skill-seekers copilot --config configs/django.json --data-dir output/django_data/

# 3. Copy to your Django project
cp output/django_copilot/.github/copilot-instructions.md ~/my-django-app/.github/

# 4. Better Django code suggestions
cd ~/my-django-app
code .
```

### For Custom Documentation

```bash
# 1. Scrape your docs
skill-seekers scrape --url https://docs.yourframework.com/ --name yourframework

# 2. Generate Copilot format
skill-seekers copilot --config output/yourframework_data/config.json --data-dir output/yourframework_data/

# 3. Use in projects
cp output/yourframework_copilot/.github/copilot-instructions.md ~/my-project/.github/
```

## What Gets Generated

### 1. `.github/copilot-instructions.md`

The main file that Copilot reads. Contains:
- **Project Overview** - What the framework/library does
- **Key Concepts** - Important concepts organized by category
- **Code Patterns** - Common coding patterns with examples
- **API Reference** - Key APIs and methods
- **Use Cases** - Common scenarios and solutions
- **Troubleshooting** - Common issues and fixes

Example structure:
```markdown
# React - GitHub Copilot Instructions

## Project Overview
React is a JavaScript library for building user interfaces...

## When to Use This Project
- Building interactive UIs
- Creating single-page applications
- Developing component-based architectures

## Key Concepts

### Components
- Functional components
- Class components
- JSX syntax

### State Management
- useState hook
- useEffect hook
- Context API

## Code Patterns

**Pattern 1**: Functional Component
```javascript
function MyComponent() {
  return <div>Hello</div>;
}
```

...
```

### 2. `.github/copilot-config.json`

Metadata about the knowledge base:
```json
{
  "name": "react",
  "description": "React framework for UIs",
  "version": "1.0.0",
  "type": "documentation",
  "language": "multi",
  "features": {
    "code_completion": true,
    "inline_documentation": true,
    "api_reference": true,
    "examples": true
  }
}
```

### 3. `docs/code-patterns.md`

Extracted code patterns from documentation:
```markdown
# React Code Patterns

## Pattern 1: Basic Component
```javascript
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

## Pattern 2: State Hook
```javascript
const [count, setCount] = useState(0);
```
```

### 4. `docs/api-reference.md`

API documentation organized for quick reference:
```markdown
# React API Reference

## Hooks

### useState
Creates a state variable...

### useEffect
Performs side effects...
```

### 5. `examples/` directory

Code examples organized by language:
- `javascript-examples.md`
- `typescript-examples.md`
- `python-examples.md`
- etc.

## Best Practices

### 1. Keep Instructions Focused

Copilot works best with concise, relevant instructions. The generator automatically:
- Limits patterns to 50 most common
- Truncates long examples
- Focuses on practical use cases

### 2. Update Regularly

As frameworks evolve:
```bash
# Re-scrape documentation
rm -rf output/react_data/
skill-seekers scrape --config configs/react.json

# Regenerate Copilot knowledge
skill-seekers copilot --config configs/react.json --data-dir output/react_data/

# Update your projects
cp output/react_copilot/.github/copilot-instructions.md ~/my-projects/*/.github/
```

### 3. Combine with Custom Instructions

You can combine generated instructions with project-specific ones:

```markdown
<!-- In your .github/copilot-instructions.md -->

# My Project - Copilot Instructions

## Project-Specific Info
This is my custom project using React...

## React Framework Knowledge
<!-- Include generated React instructions -->
```

### 4. Use Multiple Knowledge Bases

For projects using multiple frameworks:
```bash
# Generate for each framework
skill-seekers copilot --config configs/react.json --data-dir output/react_data/
skill-seekers copilot --config configs/django.json --data-dir output/django_data/

# Combine key sections
cat output/react_copilot/.github/copilot-instructions.md > my-project/.github/copilot-instructions.md
echo "\n---\n" >> my-project/.github/copilot-instructions.md
cat output/django_copilot/.github/copilot-instructions.md >> my-project/.github/copilot-instructions.md
```

## Advanced Usage

### Custom Configuration

Create a custom config for Copilot generation:

```json
{
  "name": "myframework",
  "description": "My custom framework",
  "base_url": "https://docs.myframework.com/",
  "copilot": {
    "max_patterns": 100,
    "max_examples_per_language": 30,
    "include_api_reference": true,
    "include_troubleshooting": true,
    "focus_categories": ["getting_started", "api", "patterns"]
  }
}
```

### Verbose Mode

See detailed generation information:
```bash
skill-seekers copilot --config configs/react.json --data-dir output/react_data/ --verbose
```

### Programmatic Usage

Use in Python scripts:
```python
from skill_seekers.cli.copilot_generator import CopilotKnowledgeGenerator
from pathlib import Path

config = {
    "name": "myframework",
    "description": "My framework",
    "base_url": "https://docs.myframework.com/"
}

generator = CopilotKnowledgeGenerator(config)
generator.generate(Path("output/myframework_data"))
```

## Comparison: Claude Skills vs Copilot

| Feature | Claude Skills | Copilot Knowledge |
|---------|--------------|-------------------|
| Format | `.zip` package | `.github/copilot-instructions.md` |
| Upload | To Claude AI | To your repository |
| Usage | Q&A with Claude | Code completion in IDE |
| Interactivity | High (chat) | Low (suggestions) |
| Context | Full docs | Focused patterns |
| Size | Large (MB) | Small (KB) |
| Updates | Manual reupload | Git commit |
| Sharing | Via Claude | Via repository |

**When to use Claude Skills:**
- Interactive documentation queries
- Learning and exploration
- Complex problem solving
- Natural language Q&A

**When to use Copilot Knowledge:**
- Development-time assistance
- Code completion
- Pattern following
- Quick API lookups

**Use Both:**
For the best experience, generate both formats:
```bash
# Generate Claude skill
skill-seekers scrape --config configs/react.json
skill-seekers enhance output/react/
skill-seekers package output/react/

# Generate Copilot knowledge
skill-seekers copilot --config configs/react.json --data-dir output/react_data/

# Upload Claude skill to Claude
skill-seekers upload output/react.zip

# Copy Copilot instructions to projects
cp output/react_copilot/.github/copilot-instructions.md ~/my-react-projects/*/.github/
```

## Troubleshooting

### Copilot Not Using Instructions

1. **Check file location:**
   - Must be at `.github/copilot-instructions.md`
   - Not in subdirectories

2. **Restart VS Code:**
   - Copilot reads instructions on startup
   - Restart after adding the file

3. **Check file permissions:**
   ```bash
   chmod 644 .github/copilot-instructions.md
   ```

### Instructions Too Large

GitHub Copilot has context window limits. If instructions are too large:

```bash
# Generate with fewer patterns
# Edit the generated file to keep only essential sections
nano output/react_copilot/.github/copilot-instructions.md
```

### No Code Patterns Found

If no patterns are extracted:
1. Check that documentation has code examples
2. Verify CSS selectors in config
3. Run scraper with `--verbose` flag

## Examples

### React Example

**Input:**
```bash
skill-seekers scrape --config configs/react.json
skill-seekers copilot --config configs/react.json --data-dir output/react_data/
```

**Output:** `output/react_copilot/.github/copilot-instructions.md`

### Django Example

**Input:**
```bash
skill-seekers scrape --config configs/django.json
skill-seekers copilot --config configs/django.json --data-dir output/django_data/
```

**Output:** `output/django_copilot/.github/copilot-instructions.md`

### Custom Framework Example

**Input:**
```bash
skill-seekers scrape --url https://docs.hono.dev/ --name hono
skill-seekers copilot --config output/hono_data/config.json --data-dir output/hono_data/
```

**Output:** `output/hono_copilot/.github/copilot-instructions.md`

## Learn More

- **GitHub Copilot Documentation:** https://docs.github.com/en/copilot
- **Copilot Instructions Format:** https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- **Skill Seekers Docs:** https://github.com/yusufkaraaslan/Skill_Seekers

## FAQ

**Q: Can I use both Claude Skills and Copilot together?**
A: Yes! Generate both formats for comprehensive coverage.

**Q: How often should I update Copilot instructions?**
A: Update when the framework releases major versions or API changes.

**Q: Will this work with GitHub Copilot for Business?**
A: Yes, the instructions format is the same.

**Q: Can I customize the generated instructions?**
A: Yes, edit the generated `.github/copilot-instructions.md` file.

**Q: Do I need to commit `.github/copilot-instructions.md`?**
A: Yes, commit it so all team members benefit.

---

**Happy coding with AI-powered assistance!** 🚀
