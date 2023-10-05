import openai
import wave
import pyaudio
import dotenv
import os

#dotenv.load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")

class Transcriber:
    # args: path to recording
    def __init__(self, path):
        self.path = path
        with open("transcripts/transcript.txt", "w") as f:
            f.write("")

    def transcribe(self, frames):
        self.save_audio(frames)
        transcript = openai.Audio.transcribe("whisper-1", open(self.path, "rb"))
        self.save_transcript(transcript["text"])
        return transcript["text"]
    
    def save_audio(self, frames):
        with wave.open(self.path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))

    def save_transcript(self, transcript):
        with open("transcripts/transcript.txt", "a") as f:
            f.write(transcript + "\n")

    def read_transcript(self):
        with open("transcripts/transcript.txt", "r") as f:
            return f.readlines()