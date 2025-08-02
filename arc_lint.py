#!/usr/bin/env python3

"""
Architectural Linter CLI Tool
- Meant to run in CI/CD pipeline (e.g., GitHub Actions)
- Scans all project files
- Uses OpenAI client to generate architectural review based on architect-review.md guidelines
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import argparse
from typing import List
from pathlib import Path
import re

# Load from environment (expected to be set in GitHub secrets)

# System prompt from `architect-review.md`
SYSTEM_PROMPT = """
You are an expert software architect focused on maintaining architectural integrity. Your role is to review code changes through an architectural lens, ensuring consistency with established patterns and principles.

Core Responsibilities:
1. Pattern Adherence
2. SOLID Compliance
3. Dependency Analysis
4. Abstraction Levels
5. Future-Proofing

Review Process:
1. Map the change within the overall architecture
2. Identify architectural boundaries being crossed
3. Check for consistency with existing patterns
4. Evaluate impact on system modularity
5. Suggest architectural improvements

Focus Areas:
- Service boundaries and responsibilities
- Data flow and coupling between components
- Consistency with domain-driven design (if applicable)
- Performance implications of architectural decisions
- Security boundaries and data validation points

Output Format:
- Architectural impact assessment (High/Medium/Low)
- Pattern compliance checklist
- Specific violations found (if any)
- Recommended refactoring (if needed)
- Long-term implications of the changes
- Final architectural quality score (0-100)

Remember: Good architecture enables change. Flag anything that makes future changes harder.
"""

def collect_project_files(root: str, exclude_dirs={"__pycache__", ".git", "venv"}) -> List[str]:
    """Collect all files in project"""
    files = []
    for path in Path(root).rglob("*.py"):
        if not any(part in exclude_dirs for part in path.parts):
            files.append(str(path))
    for path in Path(root).rglob("*.go"):
        if not any(part in exclude_dirs for part in path.parts):
            files.append(str(path))
    return files

def read_files(file_paths: List[str]) -> str:
    contents = []
    count = 0
    for file in file_paths:
        try:
            with open(file, 'r') as f:
                content = f"# File: {file}\n" + f.read()
                count+=len(content)
                if count>650000:
                    break
                contents.append(content)
        except Exception as e:
            print(f"Warning: Could not read file {file}: {e}")
    return "\n\n".join(contents)

def analyze_code_with_openai(code: str) -> str:
    """Send files as context to OpenAI for architectural review"""
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": code},
    ],
    temperature=0.2,
    max_tokens=4096)
    return response.choices[0].message.content

def extract_score_from_review(review: str) -> int:
    """Extracts a score from the review text (0-100) if found, else returns -1"""
    match = re.search(r"(\bscore\b|\brating\b)[^\d]{0,20}(\d{1,3})", review, re.IGNORECASE)
    if match:
        score = int(match.group(2))
        return min(max(score, 0), 100)
    return -1

def main(project_root: str, output_file: str):
    print("Collecting project files...")
    files = collect_project_files(project_root)
    print(f"Found {len(files)} files.")

    print("Reading files...")
    project_code = read_files(files)

    print("Sending to OpenAI API...")
    review = analyze_code_with_openai(project_code)

    score = extract_score_from_review(review)
    print("Writing review to output...")
    with open(output_file, "w") as f:
        f.write(review)
        f.write(f"\n\n**Overall Architectural Score: {score if score != -1 else 'Not found'} / 100**\n")

    print(f"Architectural review written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Architectural Linter with OpenAI")
    parser.add_argument("--project-root", type=str, default=".", help="Path to the root of the project")
    parser.add_argument("--output", type=str, default="architectural_review.md", help="Output markdown file")
    args = parser.parse_args()
    main(args.project_root, args.output)
