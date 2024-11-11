import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json

class Tournament:
    def __init__(self, root):
        self.root = root
        self.root.title("Турнірна Сітка")
        
        self.players = []
        self.matches = []
        self.images = {}  # Збереження зображень для учасників
        
        # Введення кількості учасників
        self.label = tk.Label(root, text="Введіть кількість учасників:")
        self.label.pack()
        self.entry = tk.Entry(root)
        self.entry.pack()
        
        self.start_button = tk.Button(root, text="Створити сітку", command=self.create_bracket)
        self.start_button.pack()
        
        # Поле для відображення переможця
        self.winner_frame = tk.Frame(root)
        self.winner_frame.pack(pady=10)
        self.winner_label = tk.Label(self.winner_frame, text="Переможець:")
        self.winner_label.pack()
        self.winner_name = tk.Label(self.winner_frame, font=("Arial", 14, "bold"))
        self.winner_name.pack()
        self.winner_image_label = tk.Label(self.winner_frame)
        self.winner_image_label.pack()
        
    def add_player(self):
        name = tk.simpledialog.askstring("Ім'я учасника", "Введіть ім'я учасника:")
        if name:
            image_path = filedialog.askopenfilename(title="Виберіть зображення учасника", 
                                                    filetypes=[("Image files", "*.jpg *.png *.jpeg")])
            if image_path:
                self.players.append((name, image_path))
                messagebox.showinfo("Учасник доданий", f"{name} доданий з зображенням.")
    
    def create_bracket(self):
        # Очищення попередніх даних
        self.players = []
        self.matches = []
        
        try:
            num_players = int(self.entry.get())
            if num_players < 2:
                raise ValueError("Кількість учасників має бути не меншою за 2.")
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірне значення: {e}")
            return
        
        # Додавання учасників із зображеннями
        for _ in range(num_players):
            self.add_player()
        
        # Створення пар для першого раунду
        self.matches = [(self.players[i], self.players[i + 1]) for i in range(0, len(self.players) - 1, 2)]
        
        # Відображення сітки
        self.display_bracket()
    
    def display_bracket(self):
        # Очищення попередньої сітки
        for widget in self.root.pack_slaves():
            if widget not in (self.entry, self.label, self.start_button, self.winner_frame):
                widget.pack_forget()
        
        self.match_buttons = []
        
        # Відображення всіх пар у першому раунді
        for match in self.matches:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            
            player1, player2 = match
            player1_name, player1_image = player1
            player2_name, player2_image = player2
            
            # Завантаження зображень
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
        winner_name, winner_image = winner
        self.players = [winner] + self.players[2:]  # Оновлення списку з переможцями
        
        # Відображення переможця
        self.winner_name.config(text=winner_name)
        img = Image.open(winner_image).resize((100, 100))
        img = ImageTk.PhotoImage(img)
        self.winner_image_label.config(image=img)
        self.winner_image_label.image = img  # Збереження посилання на зображення
        
        if len(self.players) == 1:
            messagebox.showinfo("Фінал", f"Переможець турніру: {winner_name}")
            return
        
        # Оновлення наступного раунду
        self.matches = [(self.players[i], self.players[i + 1]) for i in range(0, len(self.players) - 1, 2)]
        self.display_bracket()
    
    def save_progress(self):
        data = {
            "players": self.players,
            "matches": self.matches
        }
        with open("tournament.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Збережено", "Прогрес збережено у файл tournament.json")
    
    def load_progress(self):
        try:
            with open("tournament.json", "r") as f:
                data = json.load(f)
            self.players = data["players"]
            self.matches = data["matches"]
            self.display_bracket()
            messagebox.showinfo("Завантажено", "Прогрес турніру завантажено")
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл збереження не знайдено")

root = tk.Tk()
app = Tournament(root)

# Додамо кнопки для збереження та завантаження прогресу
save_button = tk.Button(root, text="Зберегти прогрес", command=app.save_progress)
save_button.pack()
load_button = tk.Button(root, text="Завантажити прогрес", command=app.load_progress)
load_button.pack()

root.mainloop()
