import openai
import dotenv
import os
import queue
import sys

from audio.recorder import AudioRecorder
from audio.transcriber import Transcriber
from chatgpt.completions import ChatGPT
from notes import Note, NoteStorage


dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    q = queue.Queue()
    note = NoteStorage("notes").get_note("note 1")
    recorder = AudioRecorder(q, record_length=15)
    transcriber = Transcriber("recordings/recording.wav")
    chatgpt = ChatGPT(note)
    recorder.start()
    
    try:
        while True:
            frames = q.get(block=True)
            text = transcriber.transcribe(frames)
            print(text)
            if len(text.split()) < 4:
                continue
            note.add_transcript(text)

            response = chatgpt.chat_completion(text)
            print("response:", response)
            note.add_completion(response)

            note.save()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()