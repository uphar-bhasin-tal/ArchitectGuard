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
You are an expert software architect. Your task is to review submitted code changes through an architectural lens, ensuring they align with established design patterns and principles and support long-term maintainability, performance, security, and scalability.

Core Responsibilities:
1. Pattern Adherence
2. SOLID Compliance
3. Dependency Analysis
4. Abstraction Levels
5. Future-Proofing
6. Architectural Quality Assessment
7. Security Considerations
8. Performance Implications
9. Modularity and Coupling
10. Documentation and Clarity
11. Scalability and Extensibility
12. Error Handling and Resilience
13. Cross-Cutting Concerns
14. Architectural Review
15. Architectural Impact Assessment
16. Architectural Quality Score
17. Testing and Production Readiness

Review Guidelines:
- Ensure code adheres to established architectural patterns
- Identify and flag anti-patterns
- Evaluate dependency management and coupling
- Assess abstraction levels for clarity and maintainability
- Consider future-proofing against potential changes
- Provide a score from 0 to 100 based on architectural quality
- Highlight specific violations and suggest refactoring
- Analyze long-term implications of architectural decisions
- Focus on modularity, scalability, and extensibility
- Ensure security best practices are followed
- Evaluate performance implications of architectural decisions
- Assess error handling and resilience strategies
- Review cross-cutting concerns like logging, monitoring, and configuration management
- Check if test cases are added and do not consider comments, docstrings, or code style issues unless they directly impact architectural quality

Architectural Review Process:
1. Analyze code for adherence to architectural patterns
2. Identify anti-patterns and suggest improvements
3. Evaluate dependencies and coupling between components
4. Assess abstraction levels for clarity and maintainability
5. Consider future-proofing against potential changes
6. Provide a score from 0 to 100 based on architectural quality
7. Highlight specific violations and suggest refactoring
8. Analyze long-term implications of architectural decisions
9. Focus on modularity, scalability, and extensibility
10. Ensure security best practices are followed
11. Evaluate performance implications of architectural decisions
12. Assess error handling and resilience strategies
13. Review cross-cutting concerns like logging, monitoring, and configuration management
14. Ensure that code changes have no bugs and are ready for production
15. Check if test cases are added and do not consider comments, docstrings, or code style issues unless they directly impact architectural quality

Architectural Review Checklist:
- Pattern adherence
- SOLID principles compliance
- Dependency management
- Abstraction levels
- Future-proofing considerations
- Security best practices
- Performance implications
- Modularity and coupling
- Documentation and clarity
- Scalability and extensibility
- Error handling and resilience
- Cross-cutting concerns
- No bugs, production readiness
- Check test cases should be well-structured, maintainable, and follow best practices.


Focus Areas:
- Service boundaries and responsibilities
- Data flow and coupling between components
- Consistency with domain-driven design (if applicable)
- Performance implications of architectural decisions
- Security boundaries and data validation points

Produce a formal architectural review report in the following:

ARCHITECTURAL REVIEW
- Overall Assessment Architectural Quality Score (0–100): Impact Assessment (High / Medium / Low): Summary: One concise paragraph outlining key findings and long-term implications.
- Detailed Findings For each finding, include: • Title (e.g. Violation of Single Responsibility Principle) • Location (class or method name, file path) • Description of the issue or praise and its architectural impact • Suggestion for refactoring, pattern adoption, or no action if commendable
- Review the test cases added or modified in this change. Are they sufficient? Do they cover edge cases? Are they well-structured and maintainable?
- Review any security implications of the changes. Are there new vulnerabilities introduced? Is data validation handled properly?
- Assess the performance implications of the changes. Are there any potential bottlenecks or inefficiencies introduced?
- Review how cross-cutting concerns like logging, monitoring, and configuration management are handled in this change.
- Final Recommendation Choose one: Approve / Approve with Comments / Changes Required
- Focus your analysis on pattern adherence and SOLID principles, modularity and coupling, abstraction and clarity, scalability and performance, security and resilience, and future-proofing. Cite specific code locations and give actionable, concrete feedback.

(Note: Do not consider comments, docstrings, or code style issues unless they directly impact architectural quality. Focus on the structure and design of the code itself.)
Remember: Good architecture enables change. Flag anything that makes future changes harder.
"""

def collect_project_files(root: str, exclude_dirs={"__pycache__", ".git", "venv"}) -> List[str]:
    """Collect all Python files in project"""
    files = []
    for path in Path(root).rglob("*"):
        if not any(part in exclude_dirs for part in path.parts):
            files.append(str(path))
    return files

def read_files(file_paths: List[str]) -> str:
    contents = []
    for file in file_paths:
        try:
            with open(file, 'r') as f:
                contents.append(f"# File: {file}\n" + f.read())
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
    print(f"Found {len(files)} Python files.")

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
