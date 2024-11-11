class Tournament:
    def __init__(self):
        self.players = []
        self.matches = []
        self.current_winner = None

    def add_player(self, name, image_path):
        self.players.append((name, image_path))

    def create_bracket(self):
        self.matches = [(self.players[i], self.players[i + 1]) for i in range(0, len(self.players) - 1, 2)]

    def advance_winner(self, winner):
        self.current_winner = winner
        self.players = [winner] + self.players[2:]
        self.create_bracket()

    def get_winner(self):
        return self.current_winner
    
    def reset(self):
        self.players = []
        self.matches = []
        self.current_winner = None