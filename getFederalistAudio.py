import json
import sys
import os
import boto3
import pygame
from getFederalistPaper import get_paper
from time import sleep

def text_to_speech(text: str, paper_number: int, voice_id: str = "Matthew") -> str:
    """
    Convert text to speech using Amazon Polly and save as MP3.
    Returns the path to the saved audio file.
    """
    # Create output directory if it doesn't exist
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)
    
    # Setup the output path
    output_path = os.path.join(output_dir, f"federalist_{paper_number:02d}.mp3")
    
    try:
        # Create Polly client with explicit region
        session = boto3.Session(
            region_name='us-east-1',  # You can change this to your preferred region
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        polly_client = session.client('polly')
        
        print("Generating audio... This may take a moment.")
        
        # Request speech synthesis
        response = polly_client.synthesize_speech(
            Engine='neural',
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=text
        )
        
        # Save the audio stream to file
        if "AudioStream" in response:
            with open(output_path, 'wb') as file:
                file.write(response['AudioStream'].read())
            print(f"Audio saved to: {output_path}")
            return output_path
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        if 'AWS_ACCESS_KEY_ID' not in os.environ or 'AWS_SECRET_ACCESS_KEY' not in os.environ:
            print("\nAWS credentials not found. Please set the following environment variables:")
            print("export AWS_ACCESS_KEY_ID='your_access_key'")
            print("export AWS_SECRET_ACCESS_KEY='your_secret_key'")
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
    return f"""Federalist Paper Number {paper['number']}, by {paper['author']}.
    
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