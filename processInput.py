import PyPDF2
import json
import re
import argparse
from typing import Dict, List

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from the PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"Successfully opened PDF. Number of pages: {len(pdf_reader.pages)}")
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        raise

def parse_federalist_papers(text: str, test_limit: int = None) -> List[Dict]:
    """Parse the text into individual Federalist Papers."""
    papers = []
    
    # Split text into individual papers using a more specific pattern
    paper_splits = re.split(r'(FEDERALIST\s+\d+|FEDERALIST\.?\s+No\.\s+\d+)', text)
    
    current_paper = None
    current_number = None
    
    print("\nParsing papers...")
    
    for i, split in enumerate(paper_splits):
        if not split.strip():
            continue
            
        if re.match(r'FEDERALIST\s+\d+|FEDERALIST\.?\s+No\.\s+\d+', split):
            # If we have a previous paper, save it
            if current_paper is not None:
                papers.append(current_paper)
                if test_limit and len(papers) >= test_limit:
                    break
            
            # Extract paper number
            number_match = re.search(r'\d+', split)
            if number_match:
                current_number = int(number_match.group())
                print(f"Processing paper number {current_number}")
            else:
                current_number = None
            current_paper = None
        else:
            if current_number is None:
                continue
                
            text_content = split.strip()
            
            # Try to extract author
            author_match = re.search(r'by\s+([\w\s]+)\s*\n', text_content)
            author = author_match.group(1).strip() if author_match else "Unknown"
            
            # Clean up the text
            if author_match:
                text_content = text_content.replace(author_match.group(0), '')
            
            # Remove PUBLIUS signature
            text_content = re.sub(r'\s*PUBLIUS\s*$', '', text_content)
            
            # Remove any footnotes (assuming they start with numbers in parentheses)
            text_content = re.sub(r'\(\d+\)[^\n]*\n', '', text_content)
            
            # Clean up extra whitespace
            text_content = re.sub(r'\s+', ' ', text_content)
            text_content = text_content.strip()
            
            # Create the paper entry
            current_paper = {
                "number": current_number,
                "author": author,
                "text": text_content
            }
    
    # Don't forget to append the last paper (unless we hit test_limit)
    if current_paper is not None and (not test_limit or len(papers) < test_limit):
        papers.append(current_paper)
    
    return papers

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process Federalist Papers from PDF')
    parser.add_argument('--test', type=int, help='Process only the first N papers')
    args = parser.parse_args()
    
    # Read and process the PDF
    pdf_path = "5008_Federalist Papers.pdf"
    print(f"Starting to process {pdf_path}")
    
    text = extract_text_from_pdf(pdf_path)
    
    # Parse the text into individual papers
    federalist_papers = parse_federalist_papers(text, args.test)
    
    # Sort papers by number
    federalist_papers.sort(key=lambda x: x["number"])
    
    # Print statistics
    print(f"\nProcessed {len(federalist_papers)} papers")
    
    # Save to JSON file
    output_path = "federalist_papers.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(federalist_papers, f, indent=2, ensure_ascii=False)
    
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    main()
