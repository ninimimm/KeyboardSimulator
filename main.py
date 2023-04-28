import tkinter as tk
from tkinter import ttk
import time
import json
import os


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
        self.geometry("800x400")
        self.user_statistics = user_statistics

        self.init_ui()

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

        self.label_stats = ttk.Label(self.trainer_frame, text="", font=("Arial", 14))
        self.label_stats.pack(pady=10)
        self.update_stats_label()

        self.init_trainer_widgets()

    def init_trainer_widgets(self):
        self.text_to_type = "Введите этот текст "
        self.current_position = 0
        self.start_time = None
        self.mistakes = 0

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.check_text)

        self.label_text = tk.Text(self.trainer_frame, font=("Arial", 20), height=2, width=40)
        self.label_text.insert(tk.END, self.text_to_type)
        self.label_text.configure(state='disabled')
        self.label_text.tag_configure("green", foreground="green")
        self.label_text.tag_configure("yellow", background="yellow")
        self.label_text.tag_configure("red", foreground="red")
        self.label_text.pack(pady=20)

        self.entry_text = ttk.Entry(self.trainer_frame, textvariable = self.entry_var, font = ("Arial", 20))
        self.entry_text.pack()

        self.label_result = ttk.Label(self.trainer_frame, text="", font=("Arial", 14))
        self.label_result.pack(pady=20)
        self.switch_frame_button = ttk.Button(self.trainer_frame, text="Сменить пользователя",
                                              command=self.switch_to_name_frame)
        self.switch_frame_button.pack(pady=5)

    def switch_to_trainer_frame(self):
        self.update_username()
        filename = f"{self.user_statistics.username}.json"
        existing_user_stats = UserStatistics.load_from_file(filename)
        if existing_user_stats:
            self.user_statistics = existing_user_stats
        else:
            self.user_statistics = UserStatistics(self.entry_name.get())  # create a new UserStatistics object
        self.frames["NameFrame"].pack_forget()
        self.frames["TrainerFrame"].pack(fill="both", expand=True)
        self.update_stats_label()

    def switch_to_name_frame(self):
        self.frames["TrainerFrame"].pack_forget()
        self.frames["NameFrame"].pack(fill="both", expand=True)
        self.user_statistics.save_to_file(f"{self.user_statistics.username}.json")
        self.update_stats_label()

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
                while self.label_text.get(f"1.{index}") != " " or index == len(self.text_to_type):
                    index += 1
                self.label_text.tag_add("yellow", f"1.{self.current_position}", f"1.{index}")
        else:
            wrong_pos = self.current_position
            for i in range(self.current_position):
                self.label_text.tag_add("green", f"1.{i}", f"1.{i + 1}")
            self.label_text.tag_add("red", f"1.{wrong_pos}", f"1.{self.current_position + 1}")
            mistake_char = self.text_to_type[wrong_pos]
            self.user_statistics.add_mistake(mistake_char)
            self.mistakes += 1
            self.label_result.config(text="Ошибка! Исправьте ошибку и продолжайте.", foreground="red")

        self.label_text.configure(state='disabled')

    def reset(self):
        self.entry_text.delete(0, 'end')
        self.start_time = None
        self.mistakes = 0

    def update_stats_label(self):
        mistakes_stats = ", ".join(f"{char}: {count}" for char, count in self.user_statistics.mistakes_by_char.items())
        mistakes_stats = f"Ошибки по символам: {mistakes_stats}" if mistakes_stats else "Ошибки по символам: нет"
        self.label_stats.config(text=f"Текстов набрано: {self.user_statistics.texts_typed}. "
                                     f"Средняя скорость: {self.user_statistics.get_avg_speed():.2f} зн/мин. "
                                     f"{mistakes_stats}")


if __name__ == "__main__":
    user_stats = UserStatistics("JohnDoe")
    app = KeyboardTrainer(user_stats)
    app.mainloop()

