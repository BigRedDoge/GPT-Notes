import openai


class ChatGPT:
    def __init__(self, note):
        self.note = note
        self.temperature = 0.7
        self.history_len = 5
        self.messages = [
            {"role": "system", "content": "You are a note taker. Take notes on the last prompt. Don't repeat the content of previous notes. Feel free to add any information you think is relevant."}
        ]

    def chat_completion(self, text):
        # uses last history_len messages for context
        transcript = self.note.get_transcript(self.history_len)
        completions = self.note.get_completions(self.history_len)
        print("transcript: ", transcript)
        print("completions: ", completions)
        history = self.history_len if len(completions) > self.history_len else len(completions)
        for i in range(history):
            self.messages.append({"role": "user", "content": transcript[i]})
            self.messages.append({"role": "assistant", "content": completions[i]})
        self.messages.append({"role": "user", "content": text})

        print("messages: ", self.messages)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            messages=self.messages
        )
        content = response["choices"][0]["message"]["content"]
        #self.save_message(content)
        return content
    
    def save_message(self, message):
        with open(self.completions_path, "a") as f:
            f.write(message + "\n")

    def load_messages(self, history_len=5):
        with open(self.completions_path, "r") as f:
            return f.readlines()[-history_len:]
            

