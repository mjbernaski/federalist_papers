import json
import sys
import os
import re

# Add path handling
def get_project_root():
    """Get the path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_paper(number: int) -> dict:
    """Retrieve a specific Federalist Paper from the JSON file."""
    try:
        json_path = os.path.join(get_project_root(), 'fp_tagged.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            # ... rest of function remains the same ...

def save_paper_to_txt(paper: dict, output_dir: str = "papers"):
    """Save the paper to a text file."""
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(get_project_root(), output_dir)
    os.makedirs(output_dir, exist_ok=True)
    # ... rest of function remains the same ... 