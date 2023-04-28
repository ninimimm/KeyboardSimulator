import tkinter as tk
from tkinter import ttk

class KeyboardTrainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Клавиатурный тренажер")
        self.geometry("800x200")

        self.text_to_type = "Введите этот текст"
        self.current_position = 0

        self.text_var = tk.StringVar()
        self.text_var.set(self.text_to_type)

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.check_text)

        self.label_text = ttk.Label(self, textvariable=self.text_var, font=("Arial", 20))
        self.label_text.pack(pady=20)

        self.entry_text = ttk.Entry(self, textvariable=self.entry_var, font=("Arial", 20))
        self.entry_text.pack()

        self.label_result = ttk.Label(self, text="", font=("Arial", 14))
        self.label_result.pack(pady=20)

    def check_text(self, *args):
        entered_text = self.entry_var.get()
        correct_text = self.text_to_type[: len(entered_text)]

        if entered_text == correct_text:
            self.current_position = len(entered_text)
            self.label_text.config(foreground="blue")

            if entered_text == self.text_to_type:
                self.label_result.config(text="Поздравляем, вы успешно ввели текст!", foreground="green")
        else:
            wrong_pos = self.current_position
            for i, (a, b) in enumerate(zip(entered_text, correct_text)):
                if a != b:
                    wrong_pos = i
                    break

            formatted_text = (
                self.text_to_type[:wrong_pos]
                + "\033[1;31m" + self.text_to_type[wrong_pos] + "\033[m"
                + self.text_to_type[wrong_pos + 1:]
            )

            self.label_text.config(text=formatted_text)
            self.label_result.config(text="Ошибка! Исправьте ошибку и продолжайте.", foreground="red")

if __name__ == "__main__":
    app = KeyboardTrainer()
    app.mainloop()
