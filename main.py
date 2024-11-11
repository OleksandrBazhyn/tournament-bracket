import tkinter as tk
from tournament import Tournament
from ui import TournamentUI
from data_manager import DataManager

def main():
    root = tk.Tk()
    root.title("Турнірна Сітка")
    
    # Створюємо необхідні об'єкти
    data_manager = DataManager("tournament.json")
    tournament = Tournament()
    app = TournamentUI(root, tournament, data_manager)
    
    root.mainloop()

if __name__ == "__main__":
    main()
