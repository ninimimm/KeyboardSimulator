import tkinter as tk
from tkinter import ttk
import time
import json
import os
import random
import glob

class UserStatistics:
    def __init__(self, username):
        self.username = username
        self.texts_typed = 0
        self.total_speed = 0
        self.training_history = []
        self.mistakes_by_char = {}

    def add_result(self, speed, mistakes):
        self.texts_typed += 1
        self.total_speed += speed
        self.training_history.append((speed, mistakes))

    def add_mistake(self, mistake_char):
        if mistake_char not in self.mistakes_by_char:
            self.mistakes_by_char[mistake_char] = 1
        else:
            self.mistakes_by_char[mistake_char] += 1

    def get_avg_speed(self):
        return self.total_speed / self.texts_typed if self.texts_typed > 0 else 0

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump({
                "username": self.username,
                "texts_typed": self.texts_typed,
                "total_speed": self.total_speed,
                "training_history": self.training_history,
                "mistakes_by_char": self.mistakes_by_char
            }, f)

    @classmethod
    def load_from_file(cls, filename):
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            data = json.load(f)

        user_stats = cls(data["username"])
        user_stats.texts_typed = data["texts_typed"]
        user_stats.total_speed = data["total_speed"]
        user_stats.training_history = data["training_history"]
        user_stats.mistakes_by_char = data["mistakes_by_char"]
        return user_stats

class KeyboardTrainer(tk.Tk):
    def __init__(self, user_statistics):
        super().__init__()

        self.title("Клавиатурный тренажер")
        self.geometry("1600x800")
        self.user_statistics = user_statistics
        self.is_wrong_sequence = False
        self.init_ui()

    def load_random_text(self):
        text_files = glob.glob("text/*.txt")
        if text_files:
            random_file = random.choice(text_files)
            with open(random_file, "r", encoding="utf-8") as file:
                self.text_to_type = file.read().strip()
        else:
            self.text_to_type = "No text files found in the 'text' folder."

        self.label_text.configure(state='normal')
        self.label_text.delete('1.0', tk.END)
        self.label_text.insert(tk.END, self.text_to_type)
        self.label_text.configure(state='disabled')

    def init_ui(self):
        self.frames = {}

        self.name_frame = tk.Frame(self)
        self.frames["NameFrame"] = self.name_frame
        self.frames["NameFrame"].pack(fill="both", expand=True)

        self.entry_name = ttk.Entry(self.name_frame, font=("Arial", 14))
        self.entry_name.pack(pady=10)
        self.entry_name.insert(0, self.user_statistics.username)
        self.entry_name_button = ttk.Button(self.name_frame, text="Продолжить", command=self.switch_to_trainer_frame)
        self.entry_name_button.pack(pady=5)

        self.trainer_frame = tk.Frame(self)
        self.frames["TrainerFrame"] = self.trainer_frame

        self.label_username = ttk.Label(self.trainer_frame, text=f"Пользователь: {self.user_statistics.username}", font=("Arial", 14))
        self.label_username.pack(pady=10)

        self.init_trainer_widgets()

        self.stats_frame = tk.Frame(self)
        self.frames["StatsFrame"] = self.stats_frame

        self.label_stats_title = ttk.Label(self.stats_frame, text="Статистика пользователя", font=("Arial", 14))
        self.label_stats_title.pack(pady=10)

        self.tree = ttk.Treeview(self.stats_frame, columns=("char", "count"), show="headings", height=10)
        self.tree.column("char", width=300, anchor="center")
        self.tree.column("count", width=300, anchor="center")
        self.tree.heading("char", text="Символ")
        self.tree.heading("count", text="Ошибок")
        self.tree.pack()

        self.switch_frame_button = ttk.Button(self.stats_frame, text="Вернуться к тренировке", command=self.switch_to_trainer_frame)
        self.switch_frame_button.pack(pady=5)

    def init_trainer_widgets(self):
        self.current_position = 0
        self.start_time = None
        self.mistakes = 0

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.check_text)

        self.label_text = tk.Text(self.trainer_frame, font=("Arial", 20), height=10, width=50)
        self.label_text.configure(state='disabled')
        self.label_text.tag_configure("green", foreground="green")
        self.label_text.tag_configure("yellow", background="yellow")
        self.label_text.tag_configure("red", foreground="red")
        self.label_text.pack(pady=20)

        self.entry_text = ttk.Entry(self.trainer_frame, textvariable=self.entry_var, font=("Arial", 20))
        self.entry_text.pack()

        self.label_result = ttk.Label(self.trainer_frame, text="", font=("Arial", 14))
        self.label_result.pack(pady=20)
        self.switch_frame_button = ttk.Button(self.trainer_frame, text="Сменить пользователя",
                                              command=self.switch_to_name_frame)
        self.switch_frame_button.pack(pady=5)
        self.stats_button = ttk.Button(self.trainer_frame, text="Статистика", command=self.switch_to_stats_frame)
        self.stats_button.pack(pady=5)

        self.load_random_text()

    def switch_to_trainer_frame(self):
        self.update_username()
        filename = f"{self.user_statistics.username}.json"
        existing_user_stats = UserStatistics.load_from_file(filename)
        if existing_user_stats:
            self.user_statistics = existing_user_stats
        else:
            self.user_statistics = UserStatistics(self.entry_name.get())  # create a new UserStatistics object
            self.user_statistics.save_to_file(filename)  # save the new UserStatistics object to the file
        self.frames["NameFrame"].pack_forget()
        self.frames["StatsFrame"].pack_forget()
        self.frames["TrainerFrame"].pack(fill="both", expand=True)
        self.update_stats_label()

    def switch_to_name_frame(self):
        self.user_statistics.save_to_file(f"{self.user_statistics.username}.json")
        self.frames["TrainerFrame"].pack_forget()
        self.frames["NameFrame"].pack(fill="both", expand=True)
        self.update_stats_label()

    def switch_to_stats_frame(self):
        self.user_statistics.save_to_file(f"{self.user_statistics.username}.json")
        self.frames["TrainerFrame"].pack_forget()
        self.frames["StatsFrame"].pack(fill="both", expand=True)
        self.update_stats_table()

    def update_username(self):
        self.user_statistics.username = self.entry_name.get()
        self.label_username.config(text=f"Пользователь: {self.user_statistics.username}")

    def check_text(self, *args):
        entered_text = self.entry_var.get()
        correct_text = self.text_to_type[: len(entered_text)]

        self.label_text.configure(state='normal')
        self.label_text.delete('1.0', tk.END)
        self.label_text.insert(tk.END, self.text_to_type)

        if entered_text == correct_text:
            self.is_wrong_sequence = False  # Reset the flag when the entered text is correct
            self.current_position = len(entered_text)
            if (self.current_position > 0):
                if not self.start_time:
                    self.start_time = time.time()

            if self.text_to_type.find(entered_text) != -1:
                self.label_result.config(text="Пока все правильно", foreground="green")

            if entered_text == self.text_to_type:
                self.label_result.config(text="Поздравляем, вы успешно ввели текст!", foreground="green")
                elapsed_time = time.time() - self.start_time
                speed = len(entered_text) / elapsed_time * 60 if elapsed_time > 0 else 0
                self.user_statistics.add_result(speed, self.mistakes)
                self.update_stats_label()
                self.reset()
                self.label_result.config(text=f"Скорость: {speed:.2f} зн/мин. Опечатки: {self.mistakes}",
                                         foreground="green")

            for i in range(self.current_position):
                self.label_text.tag_add("green", f"1.{i}", f"1.{i + 1}")

            if self.current_position < len(self.text_to_type):
                index = self.current_position
                while self.label_text.get(f"1.{index}") != " " and index < len(self.text_to_type):
                    index += 1
                self.label_text.tag_add("yellow", f"1.{self.current_position}", f"1.{index}")
        else:
            if not self.is_wrong_sequence:  # Only count the mistake if it's the start of the wrong sequence
                wrong_pos = self.current_position
                mistake_char = self.text_to_type[wrong_pos]
                self.user_statistics.add_mistake(mistake_char)
                self.mistakes += 1
                self.is_wrong_sequence = True  # Set the flag to avoid counting further mistakes in the current sequence

            for i in range(self.current_position):
                self.label_text.tag_add("green", f"1.{i}", f"1.{i + 1}")
            self.label_text.tag_add("red", f"1.{self.current_position}", f"1.{len(entered_text)}")
            self.label_result.config(text="Ошибка! Исправьте ошибку и продолжайте.", foreground="red")

        self.label_text.configure(state='disabled')

    def reset(self):
        self.entry_text.delete(0, 'end')
        self.start_time = None
        self.mistakes = 0
        self.load_random_text()

    def update_stats_label(self):
        avg_speed = self.user_statistics.get_avg_speed()
        self.label_result.config(text=f"Средняя скорость: {avg_speed:.2f} зн/мин. Ошибок: {self.mistakes}",
                                 foreground="green")

    def update_stats_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for char, count in self.user_statistics.mistakes_by_char.items():
            self.tree.insert("", "end", values=(char, count))
if __name__ == "__main__":
    user_stats = UserStatistics("JohnDoe")
    app = KeyboardTrainer(user_stats)
    app.mainloop()
