import json
import argparse
import re
from typing import Dict, List, Tuple

def load_papers(json_file: str = 'fp_edited.json') -> List[Dict]:
    """Load papers from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return []

def search_papers(papers: List[Dict], search_term: str, context_words: int = 10) -> List[Tuple[int, str, str]]:
    """
    Search for term in papers and return matches with context.
    Returns list of tuples: (paper_number, author, context)
    """
    results = []
    search_pattern = re.compile(r'\b' + re.escape(search_term) + r'\b', re.IGNORECASE)
    
    for paper in papers:
        matches = search_pattern.finditer(paper['text'])
        for match in matches:
            # Get the context around the match
            start_pos = max(0, match.start())
            end_pos = min(len(paper['text']), match.end())
            
            # Get words before and after
            before_text = paper['text'][:start_pos].split()[-context_words:]
            after_text = paper['text'][end_pos:].split()[:context_words]
            
            # Create context string
            context = ' '.join(before_text + 
                             [f"**{paper['text'][start_pos:end_pos]}**"] + 
                             after_text)
            
            results.append((paper['number'], paper['author'], context))
    
    return results

def save_results(results: List[Tuple[int, str, str]], search_term: str):
    """Save search results to a file."""
    output_file = f"search_results_{search_term.replace(' ', '_')}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Search Results for: '{search_term}'\n")
        f.write("=" * 80 + "\n\n")
        
        for paper_num, author, context in results:
            f.write(f"Federalist No. {paper_num} (by {author})\n")
            f.write("-" * 40 + "\n")
            f.write(f"{context}\n\n")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Search Federalist Papers for specific terms.')
    parser.add_argument('term', help='Term to search for')
    parser.add_argument('--context', type=int, default=10,
                       help='Number of context words before and after match (default: 10)')
    parser.add_argument('--json', default='fp_edited.json',
                       help='JSON file containing papers (default: fp_edited.json)')
    
    args = parser.parse_args()
    
    # Load papers
    papers = load_papers(args.json)
    if not papers:
        return
    
    # Search for term
    results = search_papers(papers, args.term, args.context)
    
    # Print results to console
    print(f"\nFound {len(results)} matches for '{args.term}'\n")
    
    if results:
        # Save to file
        output_file = save_results(results, args.term)
        
        # Print to console
        for paper_num, author, context in results:
            print(f"Federalist No. {paper_num} (by {author})")
            print("-" * 40)
            print(f"{context}\n")
        
        print(f"\nResults saved to: {output_file}")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main() 