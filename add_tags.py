import json
import ollama
import time
from typing import List
import sys

def get_tags(text: str, paper_num: int) -> List[str]:
    """Get standardized topic tags using Ollama."""
    prompt = f"""
    Read this excerpt from Federalist Paper #{paper_num} and provide 3-5 topic tags.
    Use only standardized tags from this list:
    - Federal Power
    - State Rights
    - Judiciary
    - Executive Power
    - Legislative Power
    - Military
    - Foreign Relations
    - Commerce
    - Taxation
    - Individual Rights
    - Constitutional Structure
    - Democracy
    - Republic
    - Checks and Balances
    - Federal System
    
    Text: {text[:1000]}...
    
    Return only the relevant tags as a comma-separated list, no other text.
    """
    
    try:
        print(f"\nSending request to Ollama for paper #{paper_num}...")
        response = ollama.generate(
            model='llama3.3:70b-instruct-q2_K',
            prompt=prompt
        )
        
        print(f"Raw response: {response['response']}")
        
        # Split response into tags and clean them up
        tags = [tag.strip() for tag in response['response'].split(',')]
        print(f"Split tags: {tags}")
        
        # Remove any tags not in our standardized list
        valid_tags = {
            "Federal Power", "State Rights", "Judiciary", "Executive Power",
            "Legislative Power", "Military", "Foreign Relations", "Commerce",
            "Taxation", "Individual Rights", "Constitutional Structure",
            "Democracy", "Republic", "Checks and Balances", "Federal System"
        }
        tags = [tag for tag in tags if tag in valid_tags]
        print(f"Valid tags: {tags}")
        
        return tags[:5]  # Return at most 5 tags
        
    except Exception as e:
        print(f"\nError details for paper #{paper_num}:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        return []

def main():
    # Check if Ollama is accessible
    try:
        print("Testing Ollama connection...")
        ollama.generate(model='llama3.3:70b-instruct-q2_K', prompt='test')
        print("Ollama connection successful!")
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        print("Please make sure Ollama is installed and running.")
        print("Try running: ollama pull llama3.3:70b-instruct-q2_K")
        sys.exit(1)
    
    # Read the edited JSON file
    try:
        with open('fp_edited.json', 'r', encoding='utf-8') as f:
            papers = json.load(f)
    except FileNotFoundError:
        print("Error: fp_edited.json not found. Please run clean_authors.py first.")
        sys.exit(1)
    
    total_papers = len(papers)
    tagged_papers = []
    
    print(f"\nProcessing {total_papers} papers...")
    
    for i, paper in enumerate(papers, 1):
        print(f"\nProcessing paper {i}/{total_papers}: Federalist No. {paper['number']}")
        
        # Get tags for the paper
        tags = get_tags(paper['text'], paper['number'])
        
        # Create new paper object with tags
        tagged_paper = paper.copy()
        tagged_paper['tags'] = tags
        tagged_papers.append(tagged_paper)
        
        print(f"Final tags: {', '.join(tags)}")
        
        # Add a small delay to avoid overwhelming Ollama
        time.sleep(2)
    
    # Save to new JSON file
    output_path = 'fp_tagged.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tagged_papers, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print("\nTag Statistics:")
    print("-" * 20)
    tag_counts = {}
    for paper in tagged_papers:
        for tag in paper['tags']:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{tag}: {count} papers")
    
    print(f"\nTagged file saved as: {output_path}")

if __name__ == "__main__":
    main() 