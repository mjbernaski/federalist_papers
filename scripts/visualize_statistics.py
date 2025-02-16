import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import numpy as np
import sys
import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def plot_distributions():
    # Check if statistics file exists
    stats_path = os.path.join(get_project_root(), 'statistics.csv')
    if not os.path.exists(stats_path):
        print("Error: statistics.csv not found. Please run generate_statistics.py first.")
        sys.exit(1)
    
    try:
        # Read the statistics
        df = pd.read_csv(stats_path)
        # ... rest of function remains the same ...
        
        # Save figure
        plot_path = os.path.join(get_project_root(), 'distributions.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        
        # Save tables
        table_path = os.path.join(get_project_root(), 'distribution_tables.txt')
        with open(table_path, 'w') as f:
            # ... rest of function remains the same ... 