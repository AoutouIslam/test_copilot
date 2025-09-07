class ScoreManager:
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def display_score(self):
        print(f"Score: {self.score}")

    def save_score(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self.score))

    def load_score(self, filename):
        try:
            with open(filename, 'r') as file:
                self.score = int(file.read())
        except FileNotFoundError:
            self.score = 0
        except ValueError:
            self.score = 0