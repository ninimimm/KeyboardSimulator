import tkinter as tk
from tkinter import ttk
import time

class KeyboardTrainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Клавиатурный тренажер")
        self.geometry("800x300")

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
            if entered_text == self.text_to_type[:-1]:
                self.label_result.config(text="Поздравляем, вы успешно ввели текст!", foreground="green")
                elapsed_time = time.time() - self.start_time
                speed = len(entered_text) / elapsed_time * 60
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


if __name__ == "__main__":
    app = KeyboardTrainer()
    app.mainloop()
