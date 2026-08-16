class Task:
    def __init__(self, text, done=False):
        self.text = text
        self.done = done

    def to_dict(self):
        return {"text": self.text, "done": self.done}

    @classmethod
    def from_dict(cls, data):
        return cls(data["text"], data["done"])
