import json
import time
from ollama import Client
from datetime import datetime, timedelta

def clean_text_with_ollama(text, max_retries=3, retry_delay=2):
    client = Client()
    prompt = "Clean and format the following text as a single continuous string, removing any newlines or extra spaces: " + text
    
    for attempt in range(max_retries):
        try:
            response = client.chat(model='phi4', messages=[{
                'role': 'user',
                'content': prompt
            }])
            return response.message.content.strip()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"Final attempt failed: {e}")
                return text  # Return original text if all retries fail

def process_federalist_papers():
    # Read the original file
    with open('federalist_papers.json', 'r') as file:
        papers = json.load(file)
    
    total_papers = len(papers)
    processed_papers = 0
    total_time = 0
    start_time = time.time()
    failed_papers = []
    
    # Process each paper
    for paper in papers:
        paper_start = time.time()
        print(f"\nProcessing paper {paper['number']} ({processed_papers + 1}/{total_papers})...")
        
        original_text = paper['text']
        processed_text = clean_text_with_ollama(original_text)
        
        # Check if processing actually changed the text
        if processed_text == original_text:
            failed_papers.append(paper['number'])
        
        paper['text'] = processed_text
        
        # Calculate timing metrics
        paper_duration = time.time() - paper_start
        total_time += paper_duration
        processed_papers += 1
        
        # Only include successful processing in average time calculation
        if paper_duration > 0.1:  # Threshold to detect actual processing
            # Calculate average time per paper and estimated time remaining
            avg_time_per_paper = total_time / processed_papers
            papers_remaining = total_papers - processed_papers
            estimated_time_remaining = papers_remaining * avg_time_per_paper
            
            # Format estimated completion time
            completion_time = datetime.now() + timedelta(seconds=estimated_time_remaining)
            
            print(f"Paper {paper['number']} processed in {paper_duration:.1f} seconds")
            print(f"Average processing time: {avg_time_per_paper:.1f} seconds per paper")
            print(f"Estimated time remaining: {timedelta(seconds=int(estimated_time_remaining))}")
            print(f"Estimated completion time: {completion_time.strftime('%I:%M:%S %p')}")
        else:
            print(f"Paper {paper['number']} processing failed or was too quick")
        
        time.sleep(1)  # Add a small delay to avoid overwhelming the API
    
    # Print final statistics
    total_duration = time.time() - start_time
    print(f"\nProcessing complete!")
    print(f"Total processing time: {timedelta(seconds=int(total_duration))}")
    print(f"Average time per paper: {(total_duration/total_papers):.1f} seconds")
    
    if failed_papers:
        print(f"\nWarning: The following papers may not have processed correctly: {failed_papers}")
    
    # Save the processed papers
    with open('fp_edited.json', 'w') as file:
        json.dump(papers, file, indent=2)

if __name__ == "__main__":
    process_federalist_papers() 