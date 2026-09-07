import os
import glob
from groq import Groq

def get_latest_audio_file(folder="audio"):
    files = glob.glob(os.path.join(folder, "*.wav"))
    if not files:
        raise FileNotFoundError("No audio files found in the folder.")
    return max(files, key=os.path.getctime)

def transcribe_audio():
    # Initialize the Groq client
    client = Groq()
    filename = get_latest_audio_file()  # Get the latest audio file from the "audio" folder

# Open the audio file
    with open(filename, "rb") as file:
    # Create a transcription of the audio file
      transcription = client.audio.transcriptions.create(
      file=file, # Required audio file
      model="whisper-large-v3-turbo", # Required model to use for transcription
      language="en",  
      temperature=0  
    )
    # To print only the transcription text
    print((f"Transcripted text : {transcription.text}"))
    transcription_text = transcription.text
    with open("transcript.txt", "w") as f:
        f.write(transcription_text)

    return transcription_text



