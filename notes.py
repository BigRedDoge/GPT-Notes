class NoteStorage:
    """
    Handles storage of notes
    """
    def __init__(self, path):
        self.path = path

    def get_note(self, name):
        return Note(self.path + "/" + name)

    def create_note(self, name):
        pass
    
    def delete_note(self, name):
        pass

    def list_notes(self):
        pass



class Note:
    """
    Note - stores transcript and completions
    """
    def __init__(self, path):
        self.path = path
        self.transcript = []
        self.completions = []
        self.load()

    def load(self):
        with open(self.path + "/transcript.txt", "r") as f:
            self.transcript = f.readlines()
        with open(self.path + "/completions.txt", "r") as f:
            self.completions = f.readlines()

    def save(self):
        with open(self.path + "/transcript.txt", "w") as f:
            for line in self.transcript:
                f.write(line + "\n")
        with open(self.path + "/completions.txt", "w") as f:
            for line in self.completions:
                f.write(line + "\n")

    def add_transcript(self, text):
        self.transcript.append(text)

    def add_completion(self, text):
        self.completions.append(text)
    
    def get_transcript(self, history_len=5):
        return self.transcript[-history_len:]
    
    def get_completions(self, history_len=5):
        return self.completions[-history_len:]


