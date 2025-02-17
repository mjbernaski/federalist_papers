import re
from collections import Counter
import json
from typing import Dict, List
import argparse

# Common English stop words to exclude
STOP_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for',
    'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his',
    'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
    'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
    'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like',
    'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
    'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look',
    'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two',
    'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because',
    'any', 'these', 'give', 'day', 'most', 'us', 'is', 'was', 'are', 'were', 'been',
    'has', 'had', 'shall', 'may', 'might', 'must', 'ought', 'should', 'same', 'own', 'more',
    # Previously added stop words
    'those', 'such', 'upon', 'every', 'against', 'under', 'great', 'between', 'each',
    'less', 'part', 'very', 'made', 'either', 'without', 'different', 'particular',
    'necessary', 'case', 'cases', 'number', 'subject', 'body', 'both', 'many', 'being',
    # Adding more stop words based on new output
    'much', 'too', 'several', 'far', 'latter', 'proper', 'another', 'themselves',
    'where', 'cannot', 'therefore', 'form', 'place', 'former', 'itself', 'though',
    'general', 'common', 'united', 'system', 'plan'
}

def clean_text(text: str) -> str:
    """Clean text by removing punctuation and converting to lowercase."""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_word_counts(text: str, min_length: int = 3) -> Dict[str, int]:
    """
    Count word frequencies, excluding stop words and words shorter than min_length.
    Returns dictionary of word counts sorted by frequency.
    """
    # Clean the text
    text = clean_text(text)
    
    # Split into words
    words = text.split()
    
    # Get total unique words before filtering
    total_unique_words = len(set(words))
    
    # Filter out stop words and short words
    content_words = [word for word in words 
                    if word not in STOP_WORDS 
                    and len(word) >= min_length]
    
    # Count frequencies
    word_counts = Counter(content_words)
    
    # Sort by frequency
    sorted_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))
    
    # Add total unique words count to the dictionary
    sorted_counts['__total_unique_words__'] = total_unique_words
    
    return sorted_counts

def print_top_words(word_counts: Dict[str, int], top_n: int = 50):
    """Print the top N most frequent words and their counts with percentages."""
    total_unique = word_counts.get('__total_unique_words__', 0)
    filtered_unique = len(word_counts) - 1  # Subtract 1 for the __total_unique_words__ key
    
    # Calculate total words (excluding the __total_unique_words__ count)
    total_words = sum(count for word, count in word_counts.items() 
                     if word != '__total_unique_words__')
    
    print(f"\nTotal unique words (before filtering): {total_unique}")
    print(f"Unique words (after removing stop words): {filtered_unique}")
    print(f"Total content words: {total_words}")
    print(f"\nTop {top_n} words:")
    print("-" * 45)
    print("Word               Count     % of Total")
    print("-" * 45)
    
    for i, (word, count) in enumerate(
        [(k, v) for k, v in word_counts.items() if k != '__total_unique_words__'][:top_n], 
        1
    ):
        percentage = (count / total_words) * 100
        print(f"{word:<18} {count:>5}     {percentage:>6.2f}%")

def main():
    parser = argparse.ArgumentParser(description='Analyze word frequencies in a text file.')
    parser.add_argument('file', help='Path to the text file to analyze')
    parser.add_argument('--min-length', type=int, default=3, 
                       help='Minimum word length to include (default: 3)')
    parser.add_argument('--top', type=int, default=50,
                       help='Number of top words to display (default: 50)')
    parser.add_argument('--save', action='store_true',
                       help='Save results to a JSON file')
    
    args = parser.parse_args()
    
    try:
        # Read the file
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Get word counts
        word_counts = get_word_counts(text, args.min_length)
        
        # Print results with percentages
        print_top_words(word_counts, args.top)
        
        # Optionally save to JSON
        if args.save:
            output_file = f"{args.file.rsplit('.', 1)[0]}_word_counts.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                # Calculate percentages for all words
                total_words = sum(count for word, count in word_counts.items() 
                                if word != '__total_unique_words__')
                output_data = {
                    "word_counts": word_counts,
                    "percentages": {
                        word: (count / total_words) * 100
                        for word, count in word_counts.items()
                        if word != '__total_unique_words__'
                    },
                    "total_words": total_words
                }
                json.dump(output_data, f, indent=2)
            print(f"\nWord counts and percentages saved to: {output_file}")
            
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main() 