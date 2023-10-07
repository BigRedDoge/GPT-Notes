import openai
import dotenv
import os
import queue
import sys

from audio.recorder import AudioRecorder
from audio.transcriber import Transcriber
from chatgpt.completions import ChatGPT
from notes import NoteStorage


dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    # Open a note
    note = NoteStorage("notes").get_note("note 1")
    # Queue for audio frames
    audio_queue = queue.Queue()
    # thread for recording audio
    recorder = AudioRecorder(audio_queue, record_length=15)
    # transcribes audio
    transcriber = Transcriber("recordings/recording.wav")
    # chatgpt completions api
    chatgpt = ChatGPT()
    # start audio recording thread
    recorder.start()
    
    try:
        while True:
            # get audio frames from queue
            frames = audio_queue.get(block=True)
            # transcribe audio
            text = transcriber.transcribe(frames)
            print("transcribed text: ", text)
            # if recorded speech is too short, skip
            if len(text.split()) < 4:
                continue
            # update note with transcript
            note.add_transcript(text)
            # get chatgpt response
            response = chatgpt.chat_completion(text)
            print("response: ", response)
            # update note with completion
            note.add_completion(response)
            # save note
            note.save()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()