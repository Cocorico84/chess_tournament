class Menu:
    def __init__(self):
        self.key = 0
        self.choices = {}

    def add_choice(self, description):
        self.key += 1
        self.choices[self.key] = description
