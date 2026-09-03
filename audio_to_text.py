import os
from groq import Groq


def transcribe_audio():
    # Initialize the Groq client
    client = Groq()

    # Specify the path to the audio file
    filename = os.path.dirname(__file__) + "/audio/recorded_audio.wav"

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

