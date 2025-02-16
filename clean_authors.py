import json
import re

def clean_author(author: str) -> str:
    """Clean up author field to contain only Hamilton, Madison, or Jay."""
    author = author.upper()
    
    # Define author mappings
    if 'HAMILTON' in author:
        return 'Hamilton'
    elif 'MADISON' in author:
        return 'Madison'
    elif 'JAY' in author:
        return 'Jay'
    elif 'PUBLIUS' in author:
        # You might want to handle PUBLIUS differently or do additional research
        return 'Unknown'
    else:
        return 'Unknown'

def main():
    # Read the original JSON file
    try:
        with open('federalist_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except FileNotFoundError:
        print("Error: federalist_papers.json not found.")
        return
    
    # Clean up authors
    cleaned_papers = []
    author_counts = {'Hamilton': 0, 'Madison': 0, 'Jay': 0, 'Unknown': 0}
    
    for paper in papers:
        cleaned_paper = paper.copy()
        cleaned_paper['author'] = clean_author(paper['author'])
        cleaned_papers.append(cleaned_paper)
        author_counts[cleaned_paper['author']] += 1
    
    # Save to new JSON file
    output_path = 'fp_edited.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_papers, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print("\nAuthor Statistics:")
    print("-" * 20)
    for author, count in author_counts.items():
        print(f"{author}: {count} papers")
    print(f"\nCleaned file saved as: {output_path}")

if __name__ == "__main__":
    main() 