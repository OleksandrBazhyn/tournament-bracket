import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class TournamentUI:
    def __init__(self, root, tournament, data_manager):
        self.root = root
        self.tournament = tournament
        self.data_manager = data_manager
        self.images = {}

        self.init_ui()
    
    def init_ui(self):
        # Введення кількості учасників
        self.label = tk.Label(self.root, text="Введіть кількість учасників:")
        self.label.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.start_button = tk.Button(self.root, text="Створити сітку", command=self.create_bracket)
        self.start_button.pack()

        # Поле для відображення переможця
        self.winner_frame = tk.Frame(self.root)
        self.winner_frame.pack(pady=10)
        self.winner_label = tk.Label(self.winner_frame, text="Переможець:")
        self.winner_label.pack()
        self.winner_name = tk.Label(self.winner_frame, font=("Arial", 14, "bold"))
        self.winner_name.pack()
        self.winner_image_label = tk.Label(self.winner_frame)
        self.winner_image_label.pack()

        save_button = tk.Button(self.root, text="Зберегти прогрес", command=self.save_progress)
        save_button.pack()
        load_button = tk.Button(self.root, text="Завантажити прогрес", command=self.load_progress)
        load_button.pack()

    def add_player(self):
        name = tk.simpledialog.askstring("Ім'я учасника", "Введіть ім'я учасника:")
        if name:
            image_path = filedialog.askopenfilename(title="Виберіть зображення учасника", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
            if image_path:
                self.tournament.add_player(name, image_path)
                messagebox.showinfo("Учасник доданий", f"{name} доданий з зображенням.")

    def create_bracket(self):
        try:
            num_players = int(self.entry.get())
            if num_players < 2:
                raise ValueError("Кількість учасників має бути не меншою за 2.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірне значення: {e}")
            return
        
        for _ in range(num_players):
            self.add_player()
        
        self.tournament.create_bracket()
        self.display_bracket()

    def display_bracket(self):
        # Очищення попередньої сітки
        for widget in self.root.pack_slaves():
            if widget not in (self.entry, self.label, self.start_button, self.winner_frame):
                widget.pack_forget()

        self.match_buttons = []

        for match in self.tournament.matches:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            player1, player2 = match
            player1_name, player1_image = player1
            player2_name, player2_image = player2

            img1 = Image.open(player1_image).resize((50, 50))
            img2 = Image.open(player2_image).resize((50, 50))
            img1 = ImageTk.PhotoImage(img1)
            img2 = ImageTk.PhotoImage(img2)

            self.images[player1_name] = img1
            self.images[player2_name] = img2

            tk.Label(frame, image=img1).pack(side=tk.LEFT)
            tk.Label(frame, text=f"{player1_name} vs {player2_name}").pack(side=tk.LEFT)
            tk.Label(frame, image=img2).pack(side=tk.LEFT)

            win_button1 = tk.Button(frame, text=f"Переможець: {player1_name}", command=lambda m=player1: self.advance_winner(m))
            win_button1.pack(side=tk.LEFT)
            win_button2 = tk.Button(frame, text=f"Переможець: {player2_name}", command=lambda m=player2: self.advance_winner(m))
            win_button2.pack(side=tk.LEFT)

            self.match_buttons.append((win_button1, win_button2))

    def advance_winner(self, winner):
        self.tournament.advance_winner(winner)
        winner_name, winner_image = winner
        self.winner_name.config(text=winner_name)
        img = Image.open(winner_image).resize((100, 100))
        img = ImageTk.PhotoImage(img)
        self.winner_image_label.config(image=img)
        self.winner_image_label.image = img

        if len(self.tournament.players) == 1:
            messagebox.showinfo("Фінал", f"Переможець турніру: {winner_name}")
            return

        self.display_bracket()

    def save_progress(self):
        self.data_manager.save_data(self.tournament)

    def load_progress(self):
        data = self.data_manager.load_data()
        if data:
            self.tournament.players = data["players"]
            self.tournament.matches = data["matches"]
            self.display_bracket()
