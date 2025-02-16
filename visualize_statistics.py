import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import numpy as np
import sys
import os

def create_distribution_table(data, column, bins=10):
    """Create a frequency distribution table for the given column"""
    try:
        # Calculate bins and frequencies
        hist, bin_edges = np.histogram(data[column], bins=bins)
        
        # Create bin labels
        bin_labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)]
        
        # Create distribution table
        dist_table = pd.DataFrame({
            'Range': bin_labels,
            'Frequency': hist,
            'Percentage': (hist / len(data) * 100).round(2)
        })
        
        return dist_table
    except Exception as e:
        print(f"Error creating distribution table for {column}: {str(e)}")
        sys.exit(1)

def plot_distributions():
    # Check if statistics file exists
    if not os.path.exists('statistics.csv'):
        print("Error: statistics.csv not found. Please run generate_statistics.py first.")
        sys.exit(1)
    
    try:
        # Read the statistics
        df = pd.read_csv('statistics.csv')
        
        # Set style
        plt.style.use('default')
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Word Count Distribution
        sns.histplot(data=df, x='Word Count', bins=10, ax=ax1, color='skyblue')
        ax1.set_title('Distribution of Word Counts in Federalist Papers', pad=20)
        ax1.set_xlabel('Word Count')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        
        # Character Count Distribution
        sns.histplot(data=df, x='Character Count', bins=10, ax=ax2, color='lightgreen')
        ax2.set_title('Distribution of Character Counts in Federalist Papers', pad=20)
        ax2.set_xlabel('Character Count')
        ax2.set_ylabel('Frequency')
        ax2.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
        print("Created distributions.png")
        
        # Create distribution tables
        word_dist = create_distribution_table(df, 'Word Count')
        char_dist = create_distribution_table(df, 'Character Count')
        
        # Save tables to text file
        with open('distribution_tables.txt', 'w') as f:
            f.write("Word Count Distribution\n")
            f.write("=====================\n")
            f.write(tabulate(word_dist, headers='keys', tablefmt='grid'))
            f.write("\n\nCharacter Count Distribution\n")
            f.write("==========================\n")
            f.write(tabulate(char_dist, headers='keys', tablefmt='grid'))
        print("Created distribution_tables.txt")
        
        # Print summary statistics
        print("\nWord Count Summary:")
        print(df['Word Count'].describe())
        print("\nCharacter Count Summary:")
        print(df['Character Count'].describe())
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        plt.close()

if __name__ == "__main__":
    plot_distributions() 