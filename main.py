from http import client
import time
import datetime
import sounddevice as sd
import wavio as wv
import os
import glob
from groq import Groq
from deep_translator import MyMemoryTranslator

class translating:
    def __init__(self, freq = 44100, max_duration = 300, output_folder= "audio", model = "whisper-large-v3-turbo", language="en", temperature=0,transcript_file= "transcript.txt", source = "en-GB", target= "hi-IN",translated_file="translated.txt"):
        #for recording
        self.freq = freq
        self.max_duration = max_duration
        self.output_folder = output_folder

        os.makedirs(output_folder, exist_ok=True)

        #for transcribing
        self.model = model
        self.language = language
        self.temperature = temperature
        self.transcript_file = transcript_file
        self.client = Groq()

        #for translating
        self.source = source
        self.target = target
        self.translated_file = translated_file


          # State, filled in as the pipeline runs
        self.audio_filename = None
        self.transcript = None
        self.translated_text = None

        #recording method
    def record_audio(self):
            while True:
                command = input("Enter s to start recording and q to quit: ")
        
                if command.lower() == 's':
                    print("Recording started...")
                    break
                elif command.lower() == 'q':
                    print("Exiting the program....")
                    exit()
                else:
                    print("Invalid command. Please enter 's' to start recording.")
        
            print("Recording.....Press enter to stop recording")
            recording = sd.rec(int(self.max_duration * self.freq), samplerate= self.freq, channels=1)
        
            start_time = time.time()
            input()  # Wait for user to press enter to stop recording
            sd.stop()  # Stop the recording
            duration = time.time() - start_time
        
            print("Recording stopped.")
            audio_len = int(duration * self.freq)
            recording = recording[:audio_len]
        
            # Convert the NumPy array to audio file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.output_folder, f"audio_{timestamp}.wav")
            wv.write(filename, recording, self.freq, sampwidth=2)
        
            return self.audio_filename
    
    def get_latest_audio_file(self):
        files = glob.glob(os.path.join(self.output_folder, "*.wav"))
        if not files:
            raise FileNotFoundError("No audio files found in the folder.")
        return max(files, key=os.path.getctime)

    def transcribe_audio(self):
       filename = self.get_latest_audio_file()  # Get the latest audio file from the "audio" folder

# Open the audio file
       with open(filename, "rb") as file:
    # Create a transcription of the audio file
        transcription = self.client.audio.transcriptions.create(
            file=file, # Required audio file
            model=self.model, # Required model to use for transcription
            language=self.language,  
            temperature=self.temperature)
  
    # To print only the transcription text
       print((f"Transcripted text : {transcription.text}"))
       self.transcript = transcription.text

       with open(self.transcript_file, "w") as f:
            f.write(self.transcript)

       return self.transcript


    def translate_text(self):
            """Translates the contents of self.transcript_file and saves the result."""
            translator = MyMemoryTranslator(source=self.source, target=self.target)
            self.translated_text = translator.translate_file(self.transcript_file)
 
            line = "-" * len(self.translated_text)
            print(line)
            print("Translated text: ", self.translated_text)
            print(line)
 
            with open(self.translated_file, "w") as f:
                f.write(self.translated_text)
 
            return self.translated_text
 
    def run(self):
        """Runs the full pipeline: record -> transcribe -> translate."""
        self.record_audio()
        self.transcribe_audio()
        return self.translate_text()
 
 
if __name__ == "__main__":
    pipeline = translating()
    pipeline.run()
    

    

   
         
         
         
         
    

