import json

class DataManager:
    def __init__(self, filename):
        self.filename = filename

    def save_data(self, tournament):
        data = {
            "players": tournament.players,
            "matches": tournament.matches
        }
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
