import pandas as pd
import json

def find_extreme_papers():
    """Find and display the longest and shortest Federalist Papers"""
    # Read statistics
    df = pd.read_csv('statistics.csv')
    
    # Find extremes by word count
    longest_by_words = df.loc[df['Word Count'].idxmax()]
    shortest_by_words = df.loc[df['Word Count'].idxmin()]
    
    # Find extremes by character count
    longest_by_chars = df.loc[df['Character Count'].idxmax()]
    shortest_by_chars = df.loc[df['Character Count'].idxmin()]
    
    # Get full paper content from fp_tagged.json
    with open('fp_tagged.json', 'r') as f:
        papers = json.load(f)
    
    paper_dict = {paper['number']: paper for paper in papers}
    
    # Print results
    print("\nLongest Paper by Word Count:")
    print("=" * 50)
    print(f"Paper Number: {int(longest_by_words['Paper Number'])}")
    print(f"Author: {longest_by_words['Author']}")
    print(f"Word Count: {longest_by_words['Word Count']}")
    print(f"Character Count: {longest_by_words['Character Count']}")
    if 'topics' in paper_dict[int(longest_by_words['Paper Number'])]:
        print(f"Topics: {', '.join(paper_dict[int(longest_by_words['Paper Number'])]['topics'])}")
    print("\nFirst 200 characters of text:")
    print(paper_dict[int(longest_by_words['Paper Number'])]['text'][:200] + "...")
    
    print("\nShortest Paper by Word Count:")
    print("=" * 50)
    print(f"Paper Number: {int(shortest_by_words['Paper Number'])}")
    print(f"Author: {shortest_by_words['Author']}")
    print(f"Word Count: {shortest_by_words['Word Count']}")
    print(f"Character Count: {shortest_by_words['Character Count']}")
    if 'topics' in paper_dict[int(shortest_by_words['Paper Number'])]:
        print(f"Topics: {', '.join(paper_dict[int(shortest_by_words['Paper Number'])]['topics'])}")
    print("\nFirst 200 characters of text:")
    print(paper_dict[int(shortest_by_words['Paper Number'])]['text'][:200] + "...")
    
    # Save detailed information to a file
    with open('extreme_papers.txt', 'w') as f:
        f.write("Extreme Papers in The Federalist\n")
        f.write("==============================\n\n")
        
        f.write("Longest Paper by Word Count:\n")
        f.write("=" * 50 + "\n")
        f.write(f"Paper Number: {int(longest_by_words['Paper Number'])}\n")
        f.write(f"Author: {longest_by_words['Author']}\n")
        f.write(f"Word Count: {longest_by_words['Word Count']}\n")
        f.write(f"Character Count: {longest_by_words['Character Count']}\n")
        if 'topics' in paper_dict[int(longest_by_words['Paper Number'])]:
            f.write(f"Topics: {', '.join(paper_dict[int(longest_by_words['Paper Number'])]['topics'])}\n")
        f.write("\nFull Text:\n")
        f.write(paper_dict[int(longest_by_words['Paper Number'])]['text'])
        
        f.write("\n\nShortest Paper by Word Count:\n")
        f.write("=" * 50 + "\n")
        f.write(f"Paper Number: {int(shortest_by_words['Paper Number'])}\n")
        f.write(f"Author: {shortest_by_words['Author']}\n")
        f.write(f"Word Count: {shortest_by_words['Word Count']}\n")
        f.write(f"Character Count: {shortest_by_words['Character Count']}\n")
        if 'topics' in paper_dict[int(shortest_by_words['Paper Number'])]:
            f.write(f"Topics: {', '.join(paper_dict[int(shortest_by_words['Paper Number'])]['topics'])}\n")
        f.write("\nFull Text:\n")
        f.write(paper_dict[int(shortest_by_words['Paper Number'])]['text'])

if __name__ == "__main__":
    find_extreme_papers() 