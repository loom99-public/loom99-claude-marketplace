#!/usr/bin/env python3
"""
Test Project Generator for Claude Code E2E Testing

Generates realistic test project fixtures in multiple languages (Python, JavaScript, Go)
and project types (web-app, CLI, library) for testing Claude Code plugins.

Usage:
    python generate_test_project.py --output /tmp/test-proj --type cli --language python
    python generate_test_project.py --output /tmp/web-app --type web-app --language javascript
    python generate_test_project.py --output /tmp/lib --type library --language go
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List


# ======================================================================================
# Project Templates
# ======================================================================================

PYTHON_CLI_TEMPLATE = {
    "pyproject.toml": """[project]
name = "{project_name}"
version = "0.1.0"
description = "A sample CLI application for testing"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[project.scripts]
{cli_name} = "{package_name}.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
""",
    "README.md": """# {project_name}

A sample CLI application for testing Claude Code plugins.

## Installation

```bash
pip install -e .
```

## Usage

```bash
{cli_name} --help
{cli_name} greet "World"
{cli_name} calculate 2 + 3
```

## Development

```bash
pip install -e ".[dev]"
pytest
```
""",
    "src/{package_name}/__init__.py": """\"\"\"
{project_name} - A sample CLI application
\"\"\"

__version__ = "0.1.0"
""",
    "src/{package_name}/main.py": """\"\"\"
Main CLI entry point
\"\"\"

import click

@click.group()
def cli():
    \"\"\"Sample CLI application\"\"\"
    pass


@cli.command()
@click.argument("name")
def greet(name: str):
    \"\"\"Greet someone by name\"\"\"
    message = f"Hello, {{name}}!"
    click.echo(message)
    return message


@cli.command()
@click.argument("a", type=int)
@click.argument("op")
@click.argument("b", type=int)
def calculate(a: int, op: str, b: int):
    \"\"\"Perform calculation: a op b\"\"\"
    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            click.echo("Error: Division by zero", err=True)
            return None
        result = a / b
    else:
        click.echo(f"Error: Unknown operator {{op}}", err=True)
        return None

    click.echo(f"{{a}} {{op}} {{b}} = {{result}}")
    return result


if __name__ == "__main__":
    cli()
""",
    "tests/test_main.py": """\"\"\"
Tests for main CLI module
\"\"\"

from {package_name}.main import greet, calculate


def test_greet():
    \"\"\"Test greet command\"\"\"
    result = greet("Alice")
    assert result == "Hello, Alice!"


def test_calculate_addition():
    \"\"\"Test calculate addition\"\"\"
    result = calculate(2, "+", 3)
    assert result == 5


def test_calculate_subtraction():
    \"\"\"Test calculate subtraction\"\"\"
    result = calculate(10, "-", 3)
    assert result == 7


def test_calculate_multiplication():
    \"\"\"Test calculate multiplication\"\"\"
    result = calculate(4, "*", 5)
    assert result == 20


def test_calculate_division():
    \"\"\"Test calculate division\"\"\"
    result = calculate(10, "/", 2)
    assert result == 5.0


def test_calculate_division_by_zero():
    \"\"\"Test calculate handles division by zero\"\"\"
    result = calculate(10, "/", 0)
    assert result is None
""",
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Virtual environments
venv/
.venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
"""
}

JAVASCRIPT_CLI_TEMPLATE = {
    "package.json": """{
  "name": "{project_name_slug}",
  "version": "0.1.0",
  "description": "A sample CLI application for testing",
  "main": "src/index.js",
  "bin": {
    "{cli_name}": "./bin/cli.js"
  },
  "scripts": {
    "test": "jest",
    "start": "node src/index.js"
  },
  "keywords": ["cli", "sample"],
  "author": "Test Generator",
  "license": "MIT",
  "dependencies": {
    "commander": "^11.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
""",
    "README.md": """# {project_name}

A sample CLI application for testing Claude Code plugins.

## Installation

```bash
npm install
```

## Usage

```bash
node bin/cli.js greet World
node bin/cli.js calculate 2 + 3
```

## Development

```bash
npm test
```
""",
    "bin/cli.js": """#!/usr/bin/env node

const {{ program }} = require('commander');
const {{ greet, calculate }} = require('../src/index');

program
  .name('{cli_name}')
  .description('Sample CLI application')
  .version('0.1.0');

program
  .command('greet <name>')
  .description('Greet someone by name')
  .action((name) => {{
    const message = greet(name);
    console.log(message);
  }});

program
  .command('calculate <a> <op> <b>')
  .description('Perform calculation: a op b')
  .action((a, op, b) => {{
    const result = calculate(parseInt(a), op, parseInt(b));
    if (result !== null) {{
      console.log(`${{a}} ${{op}} ${{b}} = ${{result}}`);
    }}
  }});

program.parse();
""",
    "src/index.js": """/**
 * Main module
 */

function greet(name) {
  return `Hello, ${{name}}!`;
}

function calculate(a, op, b) {
  switch (op) {
    case '+':
      return a + b;
    case '-':
      return a - b;
    case '*':
      return a * b;
    case '/':
      if (b === 0) {
        console.error('Error: Division by zero');
        return null;
      }
      return a / b;
    default:
      console.error(`Error: Unknown operator ${{op}}`);
      return null;
  }
}

module.exports = { greet, calculate };
""",
    "__tests__/index.test.js": """/**
 * Tests for main module
 */

const { greet, calculate } = require('../src/index');

describe('greet', () => {
  test('should greet by name', () => {
    expect(greet('Alice')).toBe('Hello, Alice!');
  });
});

describe('calculate', () => {
  test('should add numbers', () => {
    expect(calculate(2, '+', 3)).toBe(5);
  });

  test('should subtract numbers', () => {
    expect(calculate(10, '-', 3)).toBe(7);
  });

  test('should multiply numbers', () => {
    expect(calculate(4, '*', 5)).toBe(20);
  });

  test('should divide numbers', () => {
    expect(calculate(10, '/', 2)).toBe(5);
  });

  test('should handle division by zero', () => {
    expect(calculate(10, '/', 0)).toBeNull();
  });
});
""",
    ".gitignore": """# Dependencies
node_modules/
package-lock.json
yarn.lock

# Testing
coverage/
.nyc_output/

# Build
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
"""
}


# ======================================================================================
# Generator Functions
# ======================================================================================

def create_directory_structure(project_path: Path, template: Dict[str, str], variables: Dict[str, str]):
    """
    Create project directory structure from template.

    Args:
        project_path: Root directory for project
        template: Dictionary mapping file paths to content templates
        variables: Dictionary of template variables to substitute
    """
    project_path.mkdir(parents=True, exist_ok=True)

    for file_path_template, content_template in template.items():
        # Substitute variables in file path
        file_path_str = file_path_template.format(**variables)
        file_path = project_path / file_path_str

        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Substitute variables in content
        content = content_template.format(**variables)

        # Write file
        file_path.write_text(content)
        print(f"  Created: {file_path.relative_to(project_path)}")


def generate_python_cli(project_path: Path, project_name: str):
    """Generate Python CLI project"""
    print(f"Generating Python CLI project: {project_name}")

    package_name = project_name.lower().replace("-", "_").replace(" ", "_")
    cli_name = project_name.lower().replace(" ", "-")

    variables = {
        "project_name": project_name,
        "package_name": package_name,
        "cli_name": cli_name,
        "project_name_slug": cli_name
    }

    create_directory_structure(project_path, PYTHON_CLI_TEMPLATE, variables)
    print(f"✓ Python CLI project created at {project_path}")


def generate_javascript_cli(project_path: Path, project_name: str):
    """Generate JavaScript CLI project"""
    print(f"Generating JavaScript CLI project: {project_name}")

    cli_name = project_name.lower().replace(" ", "-")
    project_name_slug = cli_name

    variables = {
        "project_name": project_name,
        "cli_name": cli_name,
        "project_name_slug": project_name_slug
    }

    create_directory_structure(project_path, JAVASCRIPT_CLI_TEMPLATE, variables)
    print(f"✓ JavaScript CLI project created at {project_path}")


def generate_go_cli(project_path: Path, project_name: str):
    """Generate Go CLI project"""
    print(f"Generating Go CLI project: {project_name}")

    module_name = project_name.lower().replace(" ", "-")

    go_mod_template = {
        "go.mod": """module {module_name}

go 1.21

require github.com/spf13/cobra v1.7.0
""",
        "main.go": """package main

import (
\t"fmt"
\t"os"

\t"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{{
\tUse:   "{cli_name}",
\tShort: "A sample CLI application",
\tLong:  `Sample CLI application for testing Claude Code plugins.`,
}}

var greetCmd = &cobra.Command{{
\tUse:   "greet [name]",
\tShort: "Greet someone by name",
\tArgs:  cobra.ExactArgs(1),
\tRun: func(cmd *cobra.Command, args []string) {{
\t\tmessage := Greet(args[0])
\t\tfmt.Println(message)
\t}},
}}

func init() {{
\trootCmd.AddCommand(greetCmd)
}}

func main() {{
\tif err := rootCmd.Execute(); err != nil {{
\t\tfmt.Fprintln(os.Stderr, err)
\t\tos.Exit(1)
\t}}
}}

// Greet returns a greeting message
func Greet(name string) string {{
\treturn fmt.Sprintf("Hello, %s!", name)
}}

// Calculate performs arithmetic operations
func Calculate(a int, op string, b int) (int, error) {{
\tswitch op {{
\tcase "+":
\t\treturn a + b, nil
\tcase "-":
\t\treturn a - b, nil
\tcase "*":
\t\treturn a * b, nil
\tcase "/":
\t\tif b == 0 {{
\t\t\treturn 0, fmt.Errorf("division by zero")
\t\t}}
\t\treturn a / b, nil
\tdefault:
\t\treturn 0, fmt.Errorf("unknown operator: %s", op)
\t}}
}}
""",
        "main_test.go": """package main

import "testing"

func TestGreet(t *testing.T) {{
\tresult := Greet("Alice")
\texpected := "Hello, Alice!"
\tif result != expected {{
\t\tt.Errorf("Expected %s, got %s", expected, result)
\t}}
}}

func TestCalculate_Addition(t *testing.T) {{
\tresult, err := Calculate(2, "+", 3)
\tif err != nil {{
\t\tt.Errorf("Unexpected error: %v", err)
\t}}
\tif result != 5 {{
\t\tt.Errorf("Expected 5, got %d", result)
\t}}
}}

func TestCalculate_Division_ByZero(t *testing.T) {{
\t_, err := Calculate(10, "/", 0)
\tif err == nil {{
\t\tt.Error("Expected error for division by zero")
\t}}
}}
""",
        "README.md": """# {project_name}

A sample CLI application for testing Claude Code plugins.

## Installation

```bash
go build
```

## Usage

```bash
./{cli_name} greet World
```

## Testing

```bash
go test
```
""",
        ".gitignore": """# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
{cli_name}

# Test binary
*.test

# Output
*.out

# Go workspace
go.work

# IDE
.vscode/
.idea/
"""
    }

    variables = {
        "project_name": project_name,
        "module_name": module_name,
        "cli_name": module_name
    }

    create_directory_structure(project_path, go_mod_template, variables)
    print(f"✓ Go CLI project created at {project_path}")


# ======================================================================================
# Main CLI
# ======================================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate test project fixtures for Claude Code E2E testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Python CLI project
  python generate_test_project.py --output /tmp/my-cli --type cli --language python

  # Generate JavaScript CLI project
  python generate_test_project.py --output /tmp/js-app --type cli --language javascript --name "My App"

  # Generate Go CLI project
  python generate_test_project.py --output /tmp/go-tool --type cli --language go
"""
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output directory path (will be created if doesn't exist)"
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=["cli", "web-app", "library"],
        help="Project type to generate"
    )

    parser.add_argument(
        "--language",
        required=True,
        choices=["python", "javascript", "go"],
        help="Programming language"
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Project name (defaults to directory name)"
    )

    args = parser.parse_args()

    # Resolve output path
    output_path = Path(args.output).resolve()

    # Determine project name
    project_name = args.name if args.name else output_path.name.replace("-", " ").title()

    # Generate project based on language and type
    if args.language == "python" and args.type == "cli":
        generate_python_cli(output_path, project_name)
    elif args.language == "javascript" and args.type == "cli":
        generate_javascript_cli(output_path, project_name)
    elif args.language == "go" and args.type == "cli":
        generate_go_cli(output_path, project_name)
    else:
        print(f"Error: Combination not yet supported: {args.language} {args.type}", file=sys.stderr)
        print(f"Currently supported: Python/JavaScript/Go CLI projects", file=sys.stderr)
        sys.exit(1)

    print(f"\n✅ Project generated successfully!")
    print(f"   Path: {output_path}")
    print(f"   Type: {args.type}")
    print(f"   Language: {args.language}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
