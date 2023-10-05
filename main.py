import openai
import dotenv
import os
import queue

from audio.recorder import AudioRecorder
from audio.transcriber import Transcriber
from chatgpt.completions import ChatGPT


dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    q = queue.Queue()
    recorder = AudioRecorder(q, record_length=15)
    transcriber = Transcriber("recordings/recording.wav")
    chatgpt = ChatGPT()
    recorder.start()
    
    try:
        while True:
            frames = q.get(block=True)
            text = transcriber.transcribe(frames)
            print(text)
            if len(text.split()) < 4:
                continue
            response = chatgpt.chat_completion(text)
            print(response)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()