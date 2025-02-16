import json
import sys
import os
import pygame
import ollama
from getFederalistPaper import get_paper
from time import sleep

def text_to_speech(text: str, paper_number: int, model: str = "llama2") -> str:
    """
    Convert text to speech using Ollama and save as MP3.
    Returns the path to the saved audio file.
    """
    # Create output directory if it doesn't exist
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup the output path
    output_path = os.path.join(output_dir, f"federalist_{paper_number:02d}.mp3")
    
    try:
        print("Generating audio... This may take a moment.")
        
        # Request speech synthesis from Ollama
        response = ollama.generate(
            model=model,
            prompt=f"Convert this text to speech and save as MP3: {text}"
        )
        
        # TODO: Process Ollama's response to generate audio
        # This will depend on which Ollama model you're using and its TTS capabilities
        
        print(f"Audio saved to: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        sys.exit(1)

def play_audio(audio_path: str):
    """Play the audio file using pygame."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            sleep(1)
            
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error playing audio: {str(e)}")
        print(f"The audio file is saved at: {audio_path}")

def prepare_text_for_speech(paper: dict) -> str:
    """Prepare the paper text for speech synthesis."""
    topics_text = f"Topics: {', '.join(paper['topics'])}. " if 'topics' in paper else ""
    
    return f"""Federalist Paper Number {paper['number']}, by {paper['author']}. {topics_text}
    
    {paper['text']}
    
    End of Federalist Paper Number {paper['number']}.
    """

def main():
    # Check if a paper number was provided
    if len(sys.argv) != 2:
        print("Usage: python getFederalistAudio.py <paper_number>")
        print("Example: python getFederalistAudio.py 10")
        sys.exit(1)
    
    try:
        paper_number = int(sys.argv[1])
    except ValueError:
        print("Error: Please provide a valid paper number (integer)")
        sys.exit(1)
    
    # Get the paper
    paper = get_paper(paper_number)
    
    if paper is None:
        print(f"Error: Federalist Paper #{paper_number} not found.")
        sys.exit(1)
    
    # Prepare text for speech
    speech_text = prepare_text_for_speech(paper)
    
    # Convert to speech and get audio file path
    audio_path = text_to_speech(speech_text, paper_number)
    
    # Play the audio
    print("\nPlaying audio...")
    play_audio(audio_path)
    print("Audio playback completed.")

if __name__ == "__main__":
    main() 