import json
import csv

def count_stats(text):
    """Count words and characters in text"""
    # Remove extra whitespace and split into words
    words = text.strip().split()
    word_count = len(words)
    
    # Count characters (including spaces and punctuation)
    char_count = len(text)
    
    return word_count, char_count

def generate_statistics():
    # Read the tagged papers
    with open('fp_tagged.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # Prepare statistics
    stats = []
    for paper in papers:
        word_count, char_count = count_stats(paper['text'])
        stats.append({
            'paper_number': paper['number'],
            'author': paper['author'].split('\n')[0].strip(),
            'word_count': word_count,
            'character_count': char_count
        })
    
    # Sort by paper number
    stats.sort(key=lambda x: x['paper_number'])
    
    # Write to CSV
    with open('statistics.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['Paper Number', 'Author', 'Word Count', 'Character Count'])
        # Write data
        for stat in stats:
            writer.writerow([
                stat['paper_number'],
                stat['author'],
                stat['word_count'],
                stat['character_count']
            ])

if __name__ == "__main__":
    generate_statistics()
    print("Statistics have been saved to statistics.csv") 