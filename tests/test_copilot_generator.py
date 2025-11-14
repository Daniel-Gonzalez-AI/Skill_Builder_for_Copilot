"""
Tests for GitHub Copilot knowledge base generator.
"""

import pytest
import json
import tempfile
from pathlib import Path
from skill_seekers.cli.copilot_generator import CopilotKnowledgeGenerator


class TestCopilotGenerator:
    """Test the Copilot knowledge base generator."""

    def test_generator_initialization(self):
        """Test that generator initializes correctly."""
        config = {
            "name": "test-framework",
            "description": "Test framework",
            "base_url": "https://docs.test.com/"
        }
        generator = CopilotKnowledgeGenerator(config)
        
        assert generator.name == "test-framework"
        assert generator.description == "Test framework"
        assert generator.base_url == "https://docs.test.com/"

    def test_directory_structure_creation(self, tmp_path):
        """Test that output directory structure is created."""
        config = {
            "name": "test-framework",
            "description": "Test framework",
            "base_url": "https://docs.test.com/"
        }
        
        # Change output dir to temp path
        generator = CopilotKnowledgeGenerator(config)
        generator.output_dir = tmp_path / "test-framework_copilot"
        generator.github_dir = generator.output_dir / ".github"
        generator.docs_dir = generator.output_dir / "docs"
        generator.examples_dir = generator.output_dir / "examples"
        
        generator._create_directory_structure()
        
        assert generator.output_dir.exists()
        assert generator.github_dir.exists()
        assert generator.docs_dir.exists()
        assert generator.examples_dir.exists()

    def test_load_scraped_data(self, tmp_path):
        """Test loading scraped data from directory."""
        # Create fake scraped data
        data_dir = tmp_path / "test_data"
        pages_dir = data_dir / "pages"
        pages_dir.mkdir(parents=True)
        
        # Create sample page files
        page1 = {
            "url": "https://test.com/page1",
            "title": "Page 1",
            "content": "Content 1",
            "category": "getting_started"
        }
        page2 = {
            "url": "https://test.com/page2",
            "title": "Page 2",
            "content": "Content 2",
            "patterns": [
                {"code": "const x = 1;", "language": "javascript"}
            ]
        }
        
        with open(pages_dir / "page1.json", "w") as f:
            json.dump(page1, f)
        with open(pages_dir / "page2.json", "w") as f:
            json.dump(page2, f)
        
        config = {"name": "test", "description": "test", "base_url": "https://test.com"}
        generator = CopilotKnowledgeGenerator(config)
        
        pages = generator._load_scraped_data(data_dir)
        
        assert len(pages) == 2
        assert pages[0]["title"] == "Page 1" or pages[1]["title"] == "Page 1"

    def test_generate_copilot_instructions(self, tmp_path):
        """Test generation of copilot-instructions.md file."""
        config = {
            "name": "test-framework",
            "description": "Test framework for testing",
            "base_url": "https://docs.test.com/"
        }
        
        pages = [
            {
                "url": "https://test.com/page1",
                "title": "Getting Started",
                "content": "How to get started",
                "category": "getting_started",
                "patterns": []
            }
        ]
        
        generator = CopilotKnowledgeGenerator(config)
        generator.output_dir = tmp_path / "test-framework_copilot"
        generator.github_dir = generator.output_dir / ".github"
        generator.github_dir.mkdir(parents=True)
        
        generator._generate_copilot_instructions(pages)
        
        instructions_path = generator.github_dir / "copilot-instructions.md"
        assert instructions_path.exists()
        
        content = instructions_path.read_text()
        assert "Test-Framework - GitHub Copilot Instructions" in content
        assert "Project Overview" in content
        assert "Test framework for testing" in content

    def test_generate_copilot_config(self, tmp_path):
        """Test generation of copilot-config.json file."""
        config = {
            "name": "test-framework",
            "description": "Test framework",
            "base_url": "https://docs.test.com/"
        }
        
        generator = CopilotKnowledgeGenerator(config)
        generator.output_dir = tmp_path / "test-framework_copilot"
        generator.github_dir = generator.output_dir / ".github"
        generator.github_dir.mkdir(parents=True)
        
        generator._generate_copilot_config()
        
        config_path = generator.github_dir / "copilot-config.json"
        assert config_path.exists()
        
        with open(config_path) as f:
            config_data = json.load(f)
        
        assert config_data["name"] == "test-framework"
        assert config_data["description"] == "Test framework"
        assert config_data["type"] == "documentation"

    def test_extract_categories(self):
        """Test category extraction from pages."""
        config = {"name": "test", "description": "test", "base_url": "https://test.com"}
        generator = CopilotKnowledgeGenerator(config)
        
        pages = [
            {"title": "Page 1", "category": "getting_started"},
            {"title": "Page 2", "category": "getting_started"},
            {"title": "Page 3", "category": "api"},
        ]
        
        categories = generator._extract_categories(pages)
        
        assert "getting_started" in categories
        assert "api" in categories
        assert len(categories["getting_started"]) == 2
        assert len(categories["api"]) == 1

    def test_extract_code_patterns(self):
        """Test code pattern extraction from pages."""
        config = {"name": "test", "description": "test", "base_url": "https://test.com"}
        generator = CopilotKnowledgeGenerator(config)
        
        pages = [
            {
                "title": "Page 1",
                "patterns": [
                    {"code": "const x = 1;", "language": "javascript", "context": "Example 1"},
                    {"code": "const y = 2;", "language": "javascript", "context": "Example 2"}
                ]
            },
            {
                "title": "Page 2",
                "patterns": [
                    {"code": "def foo():", "language": "python", "context": "Example 3"}
                ]
            }
        ]
        
        patterns = generator._extract_code_patterns(pages)
        
        assert len(patterns) > 0
        assert any(p["language"] == "javascript" for p in patterns)

    def test_is_api_page(self):
        """Test API page detection."""
        config = {"name": "test", "description": "test", "base_url": "https://test.com"}
        generator = CopilotKnowledgeGenerator(config)
        
        api_page = {
            "title": "API Reference",
            "url": "https://test.com/api/reference",
            "category": "api"
        }
        
        non_api_page = {
            "title": "Getting Started",
            "url": "https://test.com/intro",
            "category": "tutorial"
        }
        
        assert generator._is_api_page(api_page) is True
        assert generator._is_api_page(non_api_page) is False

    def test_generate_readme(self, tmp_path):
        """Test README generation."""
        config = {
            "name": "test-framework",
            "description": "Test framework",
            "base_url": "https://docs.test.com/"
        }
        
        generator = CopilotKnowledgeGenerator(config)
        generator.output_dir = tmp_path / "test-framework_copilot"
        generator.output_dir.mkdir(parents=True)
        
        generator._generate_readme()
        
        readme_path = generator.output_dir / "README.md"
        assert readme_path.exists()
        
        content = readme_path.read_text()
        assert "Test-Framework - GitHub Copilot Knowledge Base" in content
        assert "How to Use" in content


class TestCopilotCLI:
    """Test the Copilot CLI integration."""

    def test_cli_help_output(self, capsys):
        """Test that CLI help is displayed correctly."""
        import sys
        from skill_seekers.cli.copilot_generator import main
        
        # Save original sys.argv
        original_argv = sys.argv
        
        try:
            sys.argv = ["copilot_generator.py", "--help"]
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Exit code 0 for help
            assert exc_info.value.code == 0
            
            captured = capsys.readouterr()
            assert "GitHub Copilot knowledge base" in captured.out or "GitHub Copilot knowledge base" in captured.err
        finally:
            sys.argv = original_argv

    def test_cli_requires_config(self, capsys):
        """Test that CLI requires --config argument."""
        import sys
        from skill_seekers.cli.copilot_generator import main
        
        original_argv = sys.argv
        
        try:
            sys.argv = ["copilot_generator.py", "--data-dir", "output/test_data"]
            
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Should exit with error
            assert exc_info.value.code != 0
        finally:
            sys.argv = original_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
