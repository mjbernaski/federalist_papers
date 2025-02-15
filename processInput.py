import PyPDF2
import json
import re
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

def parse_federalist_papers(text: str) -> List[Dict]:
    """Parse the text into individual Federalist Papers."""
    papers = []
    
    # Split text into individual papers using a more specific pattern
    # Looking for "FEDERALIST" followed by number
    paper_splits = re.split(r'(FEDERALIST\s+\d+|FEDERALIST\.?\s+No\.\s+\d+)', text)
    
    current_paper = None
    current_number = None
    
    print("\nDebug: Starting paper parsing")
    
    for i, split in enumerate(paper_splits):
        if not split.strip():
            continue
            
        if re.match(r'FEDERALIST\s+\d+|FEDERALIST\.?\s+No\.\s+\d+', split):
            # If we have a previous paper, save it
            if current_paper is not None:
                papers.append(current_paper)
            
            # Extract paper number
            number_match = re.search(r'\d+', split)
            if number_match:
                current_number = int(number_match.group())
                print(f"Debug: Found paper number {current_number}")
            else:
                print(f"Debug: Warning - Could not extract number from: {split}")
                current_number = None
            current_paper = None
        else:
            # This is the content of the paper
            if current_number is None:
                print(f"Debug: Skipping content without paper number")
                continue
                
            text_content = split.strip()
            
            # Try to extract author
            author_match = re.search(r'by\s+([\w\s]+)\s*\n', text_content)
            author = author_match.group(1).strip() if author_match else "Unknown"
            
            # Clean up the text by removing the author line if found
            if author_match:
                text_content = text_content.replace(author_match.group(0), '')
            
            # Remove "PUBLIUS" signature if present
            text_content = re.sub(r'\s*PUBLIUS\s*$', '', text_content)
            
            # Create the paper entry
            current_paper = {
                "number": current_number,
                "author": author,
                "text": text_content.strip()
            }
    
    # Don't forget to append the last paper
    if current_paper is not None:
        papers.append(current_paper)
    
    # Filter out any papers without numbers
    valid_papers = [p for p in papers if p["number"] is not None]
    
    if len(valid_papers) != len(papers):
        print(f"\nDebug: Filtered out {len(papers) - len(valid_papers)} invalid papers")
    
    return valid_papers

def main():
    # Read and process the PDF
    pdf_path = "5008_Federalist Papers.pdf"
    print(f"Starting to process {pdf_path}")
    
    text = extract_text_from_pdf(pdf_path)
    
    # Parse the text into individual papers
    federalist_papers = parse_federalist_papers(text)
    
    # Sort papers by number
    federalist_papers.sort(key=lambda x: x["number"])
    
    # Print some statistics
    print(f"\nFound {len(federalist_papers)} valid papers")
    if federalist_papers:
        print("\nFirst paper details:")
        print(f"Number: {federalist_papers[0]['number']}")
        print(f"Author: {federalist_papers[0]['author']}")
        print(f"Text preview: {federalist_papers[0]['text'][:200]}...")
        
        print("\nLast paper details:")
        print(f"Number: {federalist_papers[-1]['number']}")
        print(f"Author: {federalist_papers[-1]['author']}")
    else:
        print("No valid papers found!")
    
    # Save to JSON file
    output_path = "federalist_papers.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(federalist_papers, f, indent=2, ensure_ascii=False)
    
    print(f"\nOutput saved to {output_path}")

if __name__ == "__main__":
    main()
