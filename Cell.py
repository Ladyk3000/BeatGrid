class Cell:
    def __init__(self, sound=None, rect=None):
        self.sound = sound
        self.rect = rect

    def to_dict(self):
        return {
            'sound': self.sound
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sound=data.get('sound')
        )
