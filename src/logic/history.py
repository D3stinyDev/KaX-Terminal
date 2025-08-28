from collections import deque

class CommandHistory:
    def __init__(self, max_size=100):
        self.history = deque(maxlen=max_size)
        self.current_index = -1

    def add_command(self, command):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
            self.current_index = len(self.history)  # Reset index to the end

    def get_previous_command(self):
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None

    def get_next_command(self):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None

    def clear_history(self):
        self.history.clear()
        self.current_index = -1

    def get_history(self):
        return list(self.history)