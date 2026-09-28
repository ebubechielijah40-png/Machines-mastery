"""Synthetic reference; open only after investigation."""
class Machine:
    def __init__(self):
        self.position = 0

    def query(self, command):
        if command == "reset":
            self.position = 0
        elif command == "up":
            if self.position < 3:
                self.position += 1
        elif command == "down":
            if self.position > 0:
                self.position -= 1
        elif command != "peek":
            return "ERROR"
        return self.position
