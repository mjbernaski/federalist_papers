import json
import csv
import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_statistics():
    # Read the tagged papers
    json_path = os.path.join(get_project_root(), 'fp_tagged.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # ... process statistics ...
    
    # Write to CSV
    csv_path = os.path.join(get_project_root(), 'statistics.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        # ... rest of function remains the same ... 