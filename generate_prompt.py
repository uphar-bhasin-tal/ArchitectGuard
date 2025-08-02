# generate prompt based on yaml configuration
# This script generates a prompt for architectural review based on the provided YAML configuration.
# It reads the configuration from a file and constructs a prompt that can be used with an AI model.

import yaml
import argparse
from pathlib import Path
from typing import List 
import time

BASE_PROMPT = """
You are an expert software architect. Your task is to review submitted code changes through an architectural lens, ensuring they align with established design patterns and principles and support long-term maintainability, performance, security, and scalability.
(Note: Do not consider comments, docstrings, or code style issues unless they directly impact architectural quality. Focus on the structure and design of the code itself.)

"""

def load_yaml_config(file_path: str) -> dict:
    """Load YAML configuration from a file."""
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
            raise

def generate_prompt(config: dict) -> str:
    """Generate a prompt based on the YAML configuration."""

    core_resp=config.get('core_responsibilities',{})
    review_guidelines = config.get('review_guidelines', {})
    scoring = config.get('scoring', {})
    focus_areas = config.get('focus_areas', [])
    architectural_review_process = config.get('architectural_review_process', {})
    
    prompt = BASE_PROMPT
    # Add core responsibilities
    # if core_resp:
    #     prompt += "Core Responsibilities:\n"
    #     for item in core_resp:
    #         prompt += f"- {item}\n"
    
    # Add review guidelines
    if review_guidelines:
        prompt += "\nReview Guidelines:\n"
        for key, value in review_guidelines.items():
            if isinstance(value, list):
                prompt += f"- {key}:\n"
                for item in value:
                    prompt += f"  - {item}\n"
            else:
                prompt += f"- {key}: {value}\n"
    
    # Add scoring criteria
    if scoring:
        prompt += "\nScoring Criteria:\n"
        for criterion in scoring.get('criteria', []):
            prompt += f"- {criterion}\n"
    
    # Add focus areas
    if focus_areas:
        prompt += "\nFocus Areas:\n"
        for area in focus_areas:
            prompt += f"- {area}\n"
    
    # Add architectural review process steps
    if architectural_review_process:
        prompt += "\nArchitectural Review Process:\n"
        for step in architectural_review_process.get('steps', []):
            prompt += f"- {step}\n"
    
    # Add general information
    prompt += "\nGeneral Information:\n"
    prompt += f"Project Name: {config.get('project_name', 'Unknown')}\n"
    prompt += time.strftime(f"Review Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    prompt += f"Review Type: {config.get('review_type', 'Architectural')}\n"
    

    return prompt

print(generate_prompt(load_yaml_config('prompt.yaml')))