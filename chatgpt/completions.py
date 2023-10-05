import openai
import dotenv
import os

#dotenv.load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        self.temperature = 0.5
        self.history_len = 5
        self.completions_path = "transcripts/completions.txt"
        self.messages = [
            {"role": "system", "content": "You are a note taker. Take notes on the following prompts. Keep your notes concise and to the point. Don't add any extra information not in the prompt."}
        ]

    def chat_completion(self, text):
        # uses last history_len messages for context
        self.messages.append({"role": "user", "content": text})
        recent_messages = [self.messages[0]] + self.messages[-self.history_len:]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            messages=recent_messages
        )
        content = response["choices"][0]["message"]["content"]
        self.save_message(content)
        return content
    
    def save_message(self, message):
        with open(self.completions_path, "a") as f:
            f.write(message + "\n")

    def load_messages(self, history_len=5):
        with open(self.completions_path, "r") as f:
            return f.readlines()[-history_len:]
            

