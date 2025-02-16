import json
import re
from collections import Counter
import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_topic_author_matrix():
    # Read the papers
    json_path = os.path.join(get_project_root(), 'fp_tagged.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # ... process topics ...
    
    # Save output
    output_path = os.path.join(get_project_root(), 'topic_matrix.md')
    with open(output_path, 'w') as f:
        # ... rest of function remains the same ... 