import json
import os
from datetime import datetime

def get_project_root():
    """Get the path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_compilation():
    """Create a complete compilation of all Federalist Papers"""
    # Read the papers
    json_path = os.path.join(get_project_root(), 'fp_tagged.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # Sort papers by number
    papers.sort(key=lambda x: x['number'])
    
    # Create markdown version
    md_content = "# The Federalist Papers\n\n"
    md_content += f"*Compiled on {datetime.now().strftime('%B %d, %Y')}*\n\n"
    md_content += "## Table of Contents\n\n"
    
    # Create TOC
    for paper in papers:
        author = paper['author'].split('\n')[0].strip()
        md_content += f"- [Federalist No. {paper['number']}](#federalist-no-{paper['number']}) by {author}\n"
    
    md_content += "\n---\n\n"
    
    # Create text version (without markdown formatting)
    txt_content = "THE FEDERALIST PAPERS\n\n"
    txt_content += f"Compiled on {datetime.now().strftime('%B %d, %Y')}\n\n"
    txt_content += "TABLE OF CONTENTS\n\n"
    
    for paper in papers:
        author = paper['author'].split('\n')[0].strip()
        txt_content += f"Federalist No. {paper['number']} by {author}\n"
    
    txt_content += "\n" + "="*50 + "\n\n"
    
    # Add each paper
    for paper in papers:
        # Clean up author name
        author = paper['author'].split('\n')[0].strip()
        
        # Markdown version
        md_content += f"## Federalist No. {paper['number']}\n\n"
        md_content += f"**Author: {author}**\n\n"
        if 'topics' in paper:
            md_content += f"**Topics:** {', '.join(paper['topics'])}\n\n"
        if 'tags' in paper:
            md_content += f"**Tags:** {', '.join(paper['tags'])}\n\n"
        md_content += paper['text'] + "\n\n---\n\n"
        
        # Text version
        txt_content += f"FEDERALIST No. {paper['number']}\n"
        txt_content += f"Author: {author}\n"
        if 'topics' in paper:
            txt_content += f"Topics: {', '.join(paper['topics'])}\n"
        if 'tags' in paper:
            txt_content += f"Tags: {', '.join(paper['tags'])}\n"
        txt_content += "="*50 + "\n\n"
        txt_content += paper['text'] + "\n\n" + "="*50 + "\n\n"
    
    # Save markdown version
    md_path = os.path.join(get_project_root(), 'federalist_papers.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Save text version
    txt_path = os.path.join(get_project_root(), 'federalist_papers.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content)
    
    print(f"Created markdown version: {md_path}")
    print(f"Created text version: {txt_path}")

if __name__ == "__main__":
    create_compilation() 