"""Independent table representation of the specified observed contract."""
class Replica:
    TRANSITIONS = {
        "reset": (0, 0, 0, 0),
        "up": (1, 2, 3, 3),
        "down": (0, 0, 1, 2),
        "peek": (0, 1, 2, 3),
    }

    def __init__(self):
        self.state = 0

    def query(self, command):
        if command not in self.TRANSITIONS:
            return "ERROR"
        self.state = self.TRANSITIONS[command][self.state]
        return self.state
