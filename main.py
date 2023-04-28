import tkinter as tk
from tkinter import ttk
import time


class UserStatistics:
    def __init__(self, username):
        self.username = username
        self.texts_typed = 0
        self.total_speed = 0
        self.training_history = []

    def add_result(self, speed, mistakes):
        self.texts_typed += 1
        self.total_speed += speed
        self.training_history.append((speed, mistakes))

    def get_avg_speed(self):
        return self.total_speed / self.texts_typed if self.texts_typed > 0 else 0


class KeyboardTrainer(tk.Tk):
    def __init__(self, user_statistics):
        super().__init__()

        self.title("Клавиатурный тренажер")
        self.geometry("800x300")
        self.user_statistics = user_statistics
        self.label_username = ttk.Label(self, text=f"Пользователь: {self.user_statistics.username}", font=("Arial", 14))
        self.label_username.pack(pady=10)

        self.label_stats = ttk.Label(self, text="", font=("Arial", 14))
        self.label_stats.pack(pady=10)
        self.update_stats_label()

        self.init_ui()

    def init_ui(self):
        self.text_to_type = "Введите этот текст "
        self.current_position = 0
        self.start_time = None
        self.mistakes = 0

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.check_text)

        self.label_text = tk.Text(self, font=("Arial", 20), height=2, width=40)
        self.label_text.insert(tk.END, self.text_to_type)
        self.label_text.configure(state='disabled')
        self.label_text.tag_configure("green", foreground="green")
        self.label_text.tag_configure("yellow", background="yellow")
        self.label_text.tag_configure("red", foreground="red")
        self.label_text.pack(pady=20)

        self.entry_text = ttk.Entry(self, textvariable=self.entry_var, font=("Arial", 20))
        self.entry_text.pack()

        self.label_result = ttk.Label(self, text="", font=("Arial", 14))
        self.label_result.pack(pady=20)

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

                # Реализовать выход из программы

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
            self.mistakes += 1
            self.label_result.config(text="Ошибка! Исправьте ошибку и продолжайте.", foreground="red")

        self.label_text.configure(state='disabled')

    def reset(self):
        self.entry_text.delete(0, 'end')
        self.start_time = None
        self.mistakes = 0

    def update_stats_label(self):
        self.label_stats.config(text=f"Текстов набрано: {self.user_statistics.texts_typed}. "
                                     f"Средняя скорость: {self.user_statistics.get_avg_speed():.2f} зн/мин")


if __name__ == "__main__":
    user_stats = UserStatistics("JohnDoe")
    app = KeyboardTrainer(user_stats)
    app.mainloop()
