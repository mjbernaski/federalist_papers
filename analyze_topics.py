import json
import re
from collections import Counter

def extract_tags(text):
    """Extract tags from text that are marked with #tag format"""
    return set(re.findall(r'#(\w+)', text))

def create_topic_author_matrix():
    # Read the papers
    with open('federalist_papers.json', 'r') as file:
        papers = json.load(file)
    
    # Initialize counters
    authors = set()
    topics = set()
    author_count = Counter()  # Count papers by author
    topic_count = Counter()   # Count papers by topic
    author_topic_count = {}   # Count papers by author and topic
    
    for paper in papers:
        # Clean up author name
        author = paper['author'].split('\n')[0].strip()
        if 'Hamilton' in author:
            author = 'Hamilton'
        elif 'Madison' in author:
            author = 'Madison'
        elif 'Jay' in author:
            author = 'Jay'
            
        authors.add(author)
        author_count[author] += 1
        
        # Extract tags from text
        tags = extract_tags(paper['text'])
        for tag in tags:
            topics.add(tag)
            topic_count[tag] += 1
            
            # Initialize author in dict if needed
            if author not in author_topic_count:
                author_topic_count[author] = {}
            
            # Count topic for this author
            if tag not in author_topic_count[author]:
                author_topic_count[author][tag] = 0
            author_topic_count[author][tag] += 1
    
    # Generate markdown tables
    markdown = "## Papers by Author\n\n"
    markdown += "| Author | Papers |\n|---|---|\n"
    for author in sorted(authors):
        markdown += f"| {author} | {author_count[author]} |\n"
    
    markdown += "\n## Papers by Topic\n\n"
    markdown += "| Topic | Papers |\n|---|---|\n"
    for topic in sorted(topics):
        markdown += f"| {topic} | {topic_count[topic]} |\n"
    
    markdown += "\n## Papers by Author and Topic\n\n"
    markdown += "| Topic | " + " | ".join(sorted(authors)) + " |\n"
    markdown += "|" + "---|" * (len(authors) + 1) + "\n"
    
    for topic in sorted(topics):
        row = f"| {topic} |"
        for author in sorted(authors):
            count = author_topic_count.get(author, {}).get(topic, 0)
            row += f" {count} |"
        markdown += row + "\n"
    
    return markdown

if __name__ == "__main__":
    matrix = create_topic_author_matrix()
    print(matrix)
    
    # Save to file
    with open('topic_matrix.md', 'w') as f:
        f.write(matrix) 