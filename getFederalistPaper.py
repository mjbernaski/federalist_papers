import json
import sys
import os

def get_paper(number: int) -> dict:
    """Retrieve a specific Federalist Paper from the JSON file."""
    try:
        with open('federalist_papers.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
            
        # Find the paper with the specified number
        for paper in papers:
            if paper['number'] == number:
                return paper
        
        return None
    except FileNotFoundError:
        print("Error: federalist_papers.json not found. Please run processInput.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON file.")
        sys.exit(1)

def save_paper_to_txt(paper: dict, output_dir: str = "papers"):
    """Save the paper to a text file."""
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"federalist_{paper['number']:02d}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Federalist No. {paper['number']}\n")
        f.write(f"Author: {paper['author']}\n")
        f.write("=" * 50 + "\n\n")
        f.write(paper['text'])
    
    return filepath

def main():
    # Check if a paper number was provided
    if len(sys.argv) != 2:
        print("Usage: python getFederalistPaper.py <paper_number>")
        print("Example: python getFederalistPaper.py 10")
        sys.exit(1)
    
    try:
        paper_number = int(sys.argv[1])
    except ValueError:
        print("Error: Please provide a valid paper number (integer)")
        sys.exit(1)
    
    # Get the paper
    paper = get_paper(paper_number)
    
    if paper is None:
        print(f"Error: Federalist Paper #{paper_number} not found.")
        sys.exit(1)
    
    # Print to console
    print(f"\nFederalist No. {paper['number']}")
    print(f"Author: {paper['author']}")
    print("=" * 50)
    print(f"\n{paper['text']}\n")
    
    # Save to file
    filepath = save_paper_to_txt(paper)
    print(f"\nPaper has been saved to: {filepath}")

if __name__ == "__main__":
    main() 