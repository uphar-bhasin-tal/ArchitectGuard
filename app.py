import os
import subprocess
import json
from openai import OpenAI

# It is recommended to set the OPENAI_API_KEY as an environment variable
# for security reasons. The script will automatically use it.
client = OpenAI()

def get_code_snippet(file_path, line_number, context_lines=5):
    """
    Retrieves a snippet of code from a file around a specific line number.

    Args:
        file_path (str): The absolute or relative path to the file.
        line_number (int): The line number to center the snippet around.
        context_lines (int): The number of lines to include before and after the target line.

    Returns:
        str: The code snippet, or an empty string if the file cannot be read.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        snippet_lines = lines[start:end]
        return "".join(snippet_lines)
    except FileNotFoundError:
        print(f"Warning: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while reading the file {file_path}: {e}")
        return ""

def get_ai_suggestion(code_snippet, issue_description):
    """
    Sends the code snippet and issue to the OpenAI API for a replacement suggestion.

    Args:
        code_snippet (str): The piece of code that has an issue.
        issue_description (str): The description of the issue from the static analysis tool.

    Returns:
        str: The formatted suggestion from the OpenAI model.
    """
    prompt = f"""
    A Python code analysis tool reported the following issue: '{issue_description}'.
    The issue is in the following code snippet:
    
    ```python
    {code_snippet}
    ```

    Please perform the following actions:
    1. Briefly explain why this code is considered problematic (e.g., unused, deprecated).
    2. Provide the modern and corrected Python code to replace it.
    3. If the code is unused and should be deleted, just state that.
    
    Format your response clearly.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Or another suitable model like gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant that specializes in Python code refactoring."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred with the OpenAI API: {e}"

def analyze_codebase(path_to_scan):
    """
    Runs static analysis tools and then uses OpenAI to get replacement suggestions.
    
    Args:
        path_to_scan (str): The path to the Python project directory or file.
    """

    print(f"--- 1. Finding Unused Code (with Vulture) in '{path_to_scan}' ---")
    try:
        vulture_result = subprocess.run(
            ['vulture', path_to_scan, '--min-confidence', '80'],
            capture_output=True, text=True, check=True
        )
        vulture_findings = vulture_result.stdout.strip().split('\n')
        
        if vulture_findings and vulture_findings[0]:
            for finding in vulture_findings:
                try:
                    parts = finding.split(':')
                    file_path = parts[0]
                    line_number = int(parts[1])
                    description = ":".join(parts[2:]).strip()
                    
                    print("\n" + "="*50)
                    print(f"Vulture Found: Unused Code")
                    print(f"  Path: {file_path}")
                    print(f"  Line: {line_number}")
                    print(f"  Description: {description}")
                    
                    code_snippet = get_code_snippet(file_path, line_number)
                    if code_snippet:
                        ai_suggestion = get_ai_suggestion(code_snippet, f"Vulture found unused code: {description}")
                        print("\n--- OpenAI Suggestion ---")
                        print(ai_suggestion)
                        print("="*50 + "\n")

                except (ValueError, IndexError):
                    print(f"\nCould not parse vulture output line: {finding}")
        else:
            print("No unused code found by Vulture.")

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Could not run Vulture. Ensure it's installed ('pip install vulture'). Error: {e}")

    print(f"\n--- 2. Finding Deprecated Code (with Pylint) in '{path_to_scan}' ---")
    try:
        pylint_result = subprocess.run(
            ['pylint', path_to_scan, '--output-format=json'],
            capture_output=True, text=True
        )
        
        # Pylint exits with a non-zero status code if it finds issues, so we don't use check=True
        if pylint_result.stdout:
            pylint_issues = json.loads(pylint_result.stdout)
            deprecated_issues = [
                issue for issue in pylint_issues 
                if 'deprecated' in issue.get('symbol', '')
            ]

            if deprecated_issues:
                for issue in deprecated_issues:
                    file_path = issue['path']
                    line_number = issue['line']
                    description = issue['message']
                    
                    print("\n" + "="*50)
                    print(f"Pylint Found: Deprecated Code")
                    print(f"  Path: {file_path}")
                    print(f"  Line: {line_number}")
                    print(f"  Description: {description}")

                    code_snippet = get_code_snippet(file_path, line_number)
                    if code_snippet:
                        ai_suggestion = get_ai_suggestion(code_snippet, description)
                        print("\n--- OpenAI Suggestion ---")
                        print(ai_suggestion)
                        print("="*50 + "\n")
            else:
                print("No deprecated code found by Pylint.")
        else:
            print("Pylint did not produce any output.")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not run Pylint or parse its output. Ensure it's installed ('pip install pylint'). Error: {e}")


if __name__ == "__main__":
    # Change this to the path of your Python project or file
    project_path = "./sample_code/"  
    analyze_codebase(project_path)