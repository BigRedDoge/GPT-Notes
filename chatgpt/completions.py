import openai


class ChatGPT:
    def __init__(self, history_len=5):
        self.temperature = 0.7
        self.history_len = history_len
        self.messages = [
            {"role": "system", "content": "You are a note taker. Take notes on the last prompt. Don't repeat the content of previous notes. Feel free to add any information you think is relevant."}
        ]

    def chat_completion(self, text):
        # uses last history_len messages for context
        transcript = self.note.get_transcript(self.history_len)
        completions = self.note.get_completions(self.history_len)

        history = self.history_len if len(completions) > self.history_len else len(completions)
        for i in range(history):
            self.messages.append({"role": "user", "content": transcript[i]})
            self.messages.append({"role": "assistant", "content": completions[i]})
        self.messages.append({"role": "user", "content": text})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            messages=self.messages
        )
        content = response["choices"][0]["message"]["content"]

        return content
    
