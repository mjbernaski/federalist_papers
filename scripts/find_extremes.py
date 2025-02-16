import pandas as pd
import json
import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_extreme_papers():
    # Read statistics
    stats_path = os.path.join(get_project_root(), 'statistics.csv')
    df = pd.read_csv(stats_path)
    
    # Get full paper content
    json_path = os.path.join(get_project_root(), 'fp_tagged.json')
    with open(json_path, 'r') as f:
        papers = json.load(f)
    
    # ... process papers ...
    
    # Save output
    output_path = os.path.join(get_project_root(), 'extreme_papers.txt')
    with open(output_path, 'w') as f:
        # ... rest of function remains the same ... 