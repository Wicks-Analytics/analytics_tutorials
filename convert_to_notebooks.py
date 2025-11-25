"""
Script to convert Python tutorial files to Jupyter notebooks.

This script automatically converts all .py tutorial files in the tutorials/
directory to .ipynb notebook files in the notebooks/ directory.
"""

import json
import re
from pathlib import Path


def python_to_notebook(py_file: Path) -> dict:
    """
    Convert a Python tutorial file to a Jupyter notebook structure.

    Args:
        py_file: Path to Python file

    Returns:
        Dictionary representing notebook structure
    """
    with open(py_file, encoding="utf-8") as f:
        content = f.read()

    cells = []

    # Extract docstring as first markdown cell
    docstring_match = re.match(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        docstring = docstring_match.group(1).strip()
        # Convert to markdown
        lines = docstring.split("\n")
        markdown_lines = []

        for line in lines:
            line = line.strip()
            if line and "=" * 10 in line:
                continue  # Skip separator lines
            elif line:
                markdown_lines.append(line)

        # Make first line a header
        if markdown_lines:
            markdown_lines[0] = f"# {markdown_lines[0]}"

        cells.append({"cell_type": "markdown", "metadata": {}, "source": markdown_lines})

    # Split remaining content into sections
    remaining = content[docstring_match.end() :] if docstring_match else content

    # Find imports section
    imports_match = re.search(
        r"(import .*?(?=\n\ndef|\nclass|\nif __name__))", remaining, re.DOTALL
    )
    if imports_match:
        cells.append({"cell_type": "markdown", "metadata": {}, "source": ["## Setup and Imports"]})

        imports = imports_match.group(1).strip()
        # Fix path for notebooks
        imports = imports.replace(
            "project_root = Path(__file__).parent.parent.parent",
            "project_root = Path.cwd().parent.parent",
        )

        cells.append(
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": imports.split("\n"),
            }
        )

    # Find main function and extract its body
    main_match = re.search(
        r'def main\(\):.*?"""Run.*?"""(.*?)(?=\n\nif __name__|$)', remaining, re.DOTALL
    )
    if main_match:
        main_body = main_match.group(1).strip()

        # Split by step headers
        step_pattern = r'\n    # Step \d+:.*?\n    print\("\\n.*?Step \d+: (.*?)"\)'
        step_matches = list(re.finditer(step_pattern, main_body))

        for i, match in enumerate(step_matches):
            step_title = match.group(1).strip('."')

            # Get code between this step and the next
            start_pos = match.end()
            end_pos = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(main_body)
            step_code = main_body[start_pos:end_pos].strip()

            # Add markdown cell for step title
            cells.append(
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"## Step {i + 1}: {step_title}"],
                }
            )

            # Clean up the code
            code_lines = []
            for line in step_code.split("\n"):
                # Remove leading indentation (4 spaces from main function)
                if line.startswith("    "):
                    line = line[4:]

                # Skip unwanted lines
                if not line.strip():
                    continue
                if 'print("="' in line:
                    continue
                if 'print("Tutorial' in line:
                    continue
                if 'print("✅' in line:
                    continue
                if line.strip() == "return":
                    continue
                if "if __name__" in line:
                    continue

                code_lines.append(line)

            # Join and clean up the code
            if code_lines:
                code_text = "\n".join(code_lines)

                # Replace print with display for dataframes
                code_text = re.sub(r"print\(df\.head\(\)\)", "display(df.head())", code_text)
                code_text = re.sub(r"print\((\w+_df)\)", r"display(\1)", code_text)
                code_text = re.sub(
                    r"print\((\w+_result\.to_polars\(\))\)", r"display(\1)", code_text
                )

                # Remove trailing whitespace and empty lines at start/end
                code_lines_clean = [line.rstrip() for line in code_text.split("\n")]
                while code_lines_clean and not code_lines_clean[0]:
                    code_lines_clean.pop(0)
                while code_lines_clean and not code_lines_clean[-1]:
                    code_lines_clean.pop()

                if code_lines_clean:
                    cells.append(
                        {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": code_lines_clean,
                        }
                    )

    # Add exercise section if present
    if "EXERCISE" in content or "Exercise" in content:
        cells.append(
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Exercise\n", "\n", "Try the exercise below:"],
            }
        )

        cells.append(
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["# Your code here", ""],
            }
        )

    # Add key takeaways
    takeaways_match = re.search(
        r'print\("Key Takeaways:"\)(.*?)print\("\\nNext:', content, re.DOTALL
    )
    if takeaways_match:
        takeaways_lines = ["## Key Takeaways", ""]
        for line in takeaways_match.group(1).split("\n"):
            if "print(" in line:
                text_match = re.search(r'print\(f?"(.*)"\)', line)
                if text_match:
                    text = text_match.group(1)
                    # Remove escape characters
                    text = text.replace("\\n", "")
                    if text.strip():
                        takeaways_lines.append(text)

        # Find "Next:" line
        next_match = re.search(r'print\("\\nNext: (.*)"\)', content)
        if next_match:
            takeaways_lines.append("")
            takeaways_lines.append(f"**Next:** {next_match.group(1)}")

        if len(takeaways_lines) > 2:
            cells.append({"cell_type": "markdown", "metadata": {}, "source": takeaways_lines})

    # Create notebook structure
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    return notebook


def convert_all_tutorials():
    """Convert all Python tutorials to Jupyter notebooks."""

    project_root = Path(__file__).parent
    tutorials_dir = project_root / "tutorials"
    notebooks_dir = project_root / "notebooks"

    # Create notebooks directory structure
    for level in ["00_getting_started", "01_beginner", "02_intermediate", "03_advanced"]:
        (notebooks_dir / level).mkdir(parents=True, exist_ok=True)

    converted_count = 0

    # Find all Python tutorial files
    for py_file in tutorials_dir.rglob("*.py"):
        # Get relative path
        rel_path = py_file.relative_to(tutorials_dir)

        # Create corresponding notebook path
        nb_file = notebooks_dir / rel_path.with_suffix(".ipynb")

        print(f"Converting: {rel_path}")

        try:
            # Convert to notebook
            notebook = python_to_notebook(py_file)

            # Save notebook
            with open(nb_file, "w", encoding="utf-8") as f:
                json.dump(notebook, f, indent=1)

            print(f"  ✓ Created: {nb_file.relative_to(project_root)}")
            converted_count += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\n{'=' * 70}")
    print(f"✅ Converted {converted_count} tutorials to Jupyter notebooks")
    print(f"📁 Notebooks saved to: {notebooks_dir}")
    print(f"{'=' * 70}")
    print("\nTo use the notebooks:")
    print("1. Install Jupyter: pip install jupyter")
    print("2. Start Jupyter: jupyter notebook")
    print("3. Navigate to the notebooks/ folder")


if __name__ == "__main__":
    convert_all_tutorials()
