import time
import sounddevice as sd
import wavio as wv
import os


def record_audio(freq= 44100, max_duration=300):
    # Sampling frequency
    frequency = freq
    maximumum_duration = max_duration  # Maximum duration of recording in seconds
    # Create output folder if it doesn't exist
    output_folder = "audio"
    os.makedirs(output_folder, exist_ok=True)

    # Start recorder with the given values
    # of duration and sample frequency
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
    recording = sd.rec(int(maximumum_duration * frequency), samplerate=frequency, channels=1)

    start_time = time.time()
    input()  # Wait for user to press enter to stop recording
    sd.stop()  # Stop the recording
    duration = time.time() - start_time

    print("Recording stopped.")
    audio_len = int(duration * frequency)
    recording = recording[:audio_len]

    # Convert the NumPy array to audio file
    filename = os.path.join(output_folder, "recorded_audio.wav")
    wv.write(filename, recording, frequency, sampwidth=2)

    return filename



