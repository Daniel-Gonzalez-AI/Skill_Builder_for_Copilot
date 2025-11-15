#!/usr/bin/env python3
"""
GitHub Copilot Knowledge Base Generator

Converts documentation websites into GitHub Copilot-optimized knowledge bases.
Unlike Claude Skills which use .zip packages, Copilot uses:
- .github/copilot-instructions.md for project-wide context
- Inline code documentation and docstrings
- Repository structure patterns

Usage:
    skill-seekers copilot --config configs/react.json
    skill-seekers copilot --url https://react.dev/ --name react
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


class CopilotKnowledgeGenerator:
    """Generates GitHub Copilot-optimized knowledge bases from documentation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the Copilot knowledge generator.
        
        Args:
            config: Configuration dictionary with scraping parameters
        """
        self.config = config
        self.name = config['name']
        self.description = config.get('description', '')
        self.base_url = config.get('base_url', '')
        
        # Output directories
        self.output_dir = Path(f"output/{self.name}_copilot")
        self.github_dir = self.output_dir / ".github"
        self.docs_dir = self.output_dir / "docs"
        self.examples_dir = self.output_dir / "examples"
        
    def generate(self, scraped_data_dir: Path) -> None:
        """Generate Copilot knowledge base from scraped data.
        
        Args:
            scraped_data_dir: Path to directory containing scraped documentation data
        """
        logger.info(f"🤖 Generating GitHub Copilot knowledge base for {self.name}")
        
        # Create directory structure
        self._create_directory_structure()
        
        # Load scraped data
        pages_data = self._load_scraped_data(scraped_data_dir)
        
        # Generate Copilot-specific files
        self._generate_copilot_instructions(pages_data)
        self._generate_copilot_config()
        self._generate_code_patterns(pages_data)
        self._generate_api_documentation(pages_data)
        self._generate_examples(pages_data)
        self._generate_readme()
        
        logger.info(f"✅ Copilot knowledge base generated at: {self.output_dir}")
        
    def _create_directory_structure(self) -> None:
        """Create the output directory structure for Copilot."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.github_dir.mkdir(exist_ok=True)
        self.docs_dir.mkdir(exist_ok=True)
        self.examples_dir.mkdir(exist_ok=True)
        
    def _load_scraped_data(self, data_dir: Path) -> List[Dict[str, Any]]:
        """Load scraped pages from data directory.
        
        Args:
            data_dir: Path to scraped data directory
            
        Returns:
            List of page dictionaries
        """
        pages = []
        pages_dir = data_dir / "pages"
        
        if not pages_dir.exists():
            logger.warning(f"⚠️  No pages directory found at {pages_dir}")
            return pages
            
        for page_file in pages_dir.glob("*.json"):
            try:
                with open(page_file, 'r', encoding='utf-8') as f:
                    page_data = json.load(f)
                    pages.append(page_data)
            except Exception as e:
                logger.warning(f"⚠️  Failed to load {page_file}: {e}")
                
        logger.info(f"📄 Loaded {len(pages)} pages from {data_dir}")
        return pages
        
    def _generate_copilot_instructions(self, pages: List[Dict[str, Any]]) -> None:
        """Generate .github/copilot-instructions.md file.
        
        This is the main file that GitHub Copilot reads for project context.
        
        Args:
            pages: List of scraped page data
        """
        instructions_path = self.github_dir / "copilot-instructions.md"
        
        # Extract key concepts and patterns
        categories = self._extract_categories(pages)
        code_patterns = self._extract_code_patterns(pages)
        api_endpoints = self._extract_api_endpoints(pages)
        
        content = f"""# {self.name.title()} - GitHub Copilot Instructions

## Project Overview

{self.description}

**Base URL:** {self.base_url}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Pages:** {len(pages)}

## When to Use This Project

This project provides comprehensive knowledge about {self.name.title()} to help you:
- Write code following {self.name} best practices
- Use {self.name} APIs and patterns correctly
- Understand common use cases and examples
- Debug and troubleshoot {self.name}-related issues

## Project Structure

```
{self.name}/
├── docs/              # Comprehensive documentation
├── examples/          # Code examples and patterns
└── .github/
    ├── copilot-instructions.md   # This file
    └── copilot-config.json       # Copilot configuration
```

## Key Concepts and Categories

{self._format_categories(categories)}

## Code Patterns and Best Practices

{self._format_code_patterns(code_patterns)}

## API Reference

{self._format_api_endpoints(api_endpoints)}

## Common Use Cases

{self._format_use_cases(pages)}

## Troubleshooting Guidelines

When encountering issues with {self.name}:
1. Check the API documentation in `docs/api.md`
2. Review examples in `examples/` directory
3. Verify configuration against best practices
4. Consult error messages in documentation

## Additional Resources

- Full documentation: See `docs/` directory
- Code examples: See `examples/` directory
- Official docs: {self.base_url}

---

*This file is optimized for GitHub Copilot to provide context-aware code suggestions.*
"""
        
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.info(f"✅ Generated copilot-instructions.md")
        
    def _generate_copilot_config(self) -> None:
        """Generate .github/copilot-config.json configuration file."""
        config_path = self.github_dir / "copilot-config.json"
        
        config = {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0",
            "type": "documentation",
            "language": "multi",
            "documentation_url": self.base_url,
            "generated_at": datetime.now().isoformat(),
            "features": {
                "code_completion": True,
                "inline_documentation": True,
                "api_reference": True,
                "examples": True
            }
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        logger.info(f"✅ Generated copilot-config.json")
        
    def _generate_code_patterns(self, pages: List[Dict[str, Any]]) -> None:
        """Generate code patterns documentation.
        
        Args:
            pages: List of scraped page data
        """
        patterns_path = self.docs_dir / "code-patterns.md"
        
        patterns = []
        for page in pages:
            if 'patterns' in page and page['patterns']:
                patterns.extend(page['patterns'])
                
        content = f"""# {self.name.title()} Code Patterns

This document contains common code patterns and examples for {self.name}.

## Overview

Total patterns extracted: {len(patterns)}

## Patterns

"""
        
        for i, pattern in enumerate(patterns[:50], 1):  # Limit to 50 patterns
            code = pattern.get('code', '')
            language = pattern.get('language', 'text')
            context = pattern.get('context', '')
            
            content += f"""### Pattern {i}

{context}

```{language}
{code}
```

---

"""
        
        with open(patterns_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.info(f"✅ Generated code-patterns.md with {len(patterns)} patterns")
        
    def _generate_api_documentation(self, pages: List[Dict[str, Any]]) -> None:
        """Generate API reference documentation.
        
        Args:
            pages: List of scraped page data
        """
        api_path = self.docs_dir / "api-reference.md"
        
        # Filter pages that look like API documentation
        api_pages = [p for p in pages if self._is_api_page(p)]
        
        content = f"""# {self.name.title()} API Reference

Comprehensive API reference for {self.name}.

## Overview

Total API pages: {len(api_pages)}

## API Endpoints and Methods

"""
        
        for page in api_pages[:100]:  # Limit to 100 pages
            title = page.get('title', 'Untitled')
            url = page.get('url', '')
            content_preview = page.get('content', '')[:500]
            
            content += f"""### {title}

**URL:** {url}

{content_preview}

---

"""
        
        with open(api_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.info(f"✅ Generated api-reference.md with {len(api_pages)} API pages")
        
    def _generate_examples(self, pages: List[Dict[str, Any]]) -> None:
        """Generate code examples.
        
        Args:
            pages: List of scraped page data
        """
        # Extract unique code examples
        examples = {}
        for page in pages:
            if 'patterns' in page:
                for pattern in page['patterns']:
                    language = pattern.get('language', 'text')
                    code = pattern.get('code', '')
                    if code and len(code) > 50:  # Only substantial examples
                        if language not in examples:
                            examples[language] = []
                        examples[language].append({
                            'code': code,
                            'source': page.get('title', 'Unknown'),
                            'url': page.get('url', '')
                        })
        
        # Generate example files by language
        for language, code_examples in examples.items():
            example_path = self.examples_dir / f"{language}-examples.md"
            
            content = f"""# {self.name.title()} {language.title()} Examples

Code examples extracted from documentation.

## Examples

"""
            
            for i, example in enumerate(code_examples[:20], 1):  # Limit to 20 per language
                content += f"""### Example {i}: {example['source']}

Source: {example['url']}

```{language}
{example['code']}
```

---

"""
            
            with open(example_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            logger.info(f"✅ Generated {language}-examples.md with {len(code_examples)} examples")
            
    def _generate_readme(self) -> None:
        """Generate README.md for the Copilot knowledge base."""
        readme_path = self.output_dir / "README.md"
        
        content = f"""# {self.name.title()} - GitHub Copilot Knowledge Base

This directory contains a GitHub Copilot-optimized knowledge base for {self.name}.

## What's Inside

- **`.github/copilot-instructions.md`** - Main instruction file for Copilot
- **`.github/copilot-config.json`** - Configuration metadata
- **`docs/`** - Comprehensive documentation
  - `code-patterns.md` - Common code patterns
  - `api-reference.md` - API documentation
- **`examples/`** - Code examples by language

## How to Use

### Option 1: Copy to Your Project

Copy the `.github/copilot-instructions.md` file to your project's `.github/` directory:

```bash
cp {self.name}_copilot/.github/copilot-instructions.md your-project/.github/
```

### Option 2: Reference in Your Repository

Keep this as a separate repository and reference it in your project's documentation.

### Option 3: Use as Copilot Extension (Future)

GitHub Copilot may support custom knowledge bases in the future.

## About GitHub Copilot Instructions

GitHub Copilot reads `.github/copilot-instructions.md` to understand your project context and provide better code suggestions.

## Generated Information

- **Source:** {self.base_url}
- **Generated:** {datetime.now().strftime('%Y-%m-%d')}
- **Tool:** Skill Seekers (Copilot Mode)

## Learn More

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Original Documentation]({self.base_url})

---

Generated by [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - Documentation to Copilot Knowledge Base converter
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.info(f"✅ Generated README.md")
        
    # Helper methods
    
    def _extract_categories(self, pages: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Extract categories from pages."""
        categories = {}
        for page in pages:
            category = page.get('category', 'uncategorized')
            if category not in categories:
                categories[category] = []
            categories[category].append(page.get('title', 'Untitled'))
        return categories
        
    def _extract_code_patterns(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract code patterns from pages."""
        patterns = []
        for page in pages:
            if 'patterns' in page and page['patterns']:
                patterns.extend(page['patterns'][:5])  # Max 5 per page
        return patterns[:100]  # Limit total
        
    def _extract_api_endpoints(self, pages: List[Dict[str, Any]]) -> List[str]:
        """Extract API endpoints from pages."""
        endpoints = []
        for page in pages:
            if self._is_api_page(page):
                endpoints.append(page.get('title', 'Unknown API'))
        return endpoints[:50]  # Limit
        
    def _is_api_page(self, page: Dict[str, Any]) -> bool:
        """Check if page is an API reference page."""
        title = page.get('title', '').lower()
        url = page.get('url', '').lower()
        category = page.get('category', '').lower()
        
        api_keywords = ['api', 'reference', 'method', 'function', 'class', 'endpoint']
        return any(keyword in title or keyword in url or keyword in category 
                   for keyword in api_keywords)
        
    def _format_categories(self, categories: Dict[str, List[str]]) -> str:
        """Format categories for markdown."""
        if not categories:
            return "No categories found."
            
        content = ""
        for category, pages in list(categories.items())[:10]:  # Limit to 10 categories
            content += f"\n### {category.title()}\n\n"
            for page in pages[:5]:  # Limit to 5 pages per category
                content += f"- {page}\n"
            content += "\n"
        return content
        
    def _format_code_patterns(self, patterns: List[Dict[str, Any]]) -> str:
        """Format code patterns for markdown."""
        if not patterns:
            return "No code patterns found."
            
        content = ""
        for i, pattern in enumerate(patterns[:10], 1):  # Limit to 10
            code = pattern.get('code', '')[:200]  # Truncate
            language = pattern.get('language', 'text')
            content += f"\n**Pattern {i}** ({language}):\n```{language}\n{code}\n```\n\n"
        return content
        
    def _format_api_endpoints(self, endpoints: List[str]) -> str:
        """Format API endpoints for markdown."""
        if not endpoints:
            return "No API endpoints found."
            
        content = ""
        for endpoint in endpoints[:20]:  # Limit to 20
            content += f"- {endpoint}\n"
        return content
        
    def _format_use_cases(self, pages: List[Dict[str, Any]]) -> str:
        """Format common use cases for markdown."""
        # Look for tutorial or guide pages
        use_case_pages = [p for p in pages 
                          if any(keyword in p.get('title', '').lower() 
                                for keyword in ['tutorial', 'guide', 'how to', 'getting started'])]
        
        if not use_case_pages:
            return f"Refer to the documentation at {self.base_url} for use cases."
            
        content = ""
        for page in use_case_pages[:10]:  # Limit to 10
            title = page.get('title', 'Untitled')
            url = page.get('url', '')
            content += f"- **{title}**: {url}\n"
        return content


def main():
    """Main entry point for Copilot generator CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate GitHub Copilot knowledge base from documentation"
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration JSON file'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        required=True,
        help='Path to scraped data directory (e.g., output/react_data)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(message)s'
    )
    
    # Load config
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        print("❌ Error: --config is required")
        sys.exit(1)
        
    # Generate Copilot knowledge base
    generator = CopilotKnowledgeGenerator(config)
    generator.generate(Path(args.data_dir))
    
    print("\n🎉 Done! Your Copilot knowledge base is ready.")
    print(f"\n📁 Location: output/{config['name']}_copilot/")
    print("\n📖 Next steps:")
    print("   1. Copy .github/copilot-instructions.md to your project")
    print("   2. GitHub Copilot will automatically use it for context")
    print("   3. Start coding with better AI suggestions!")


if __name__ == '__main__':
    main()
