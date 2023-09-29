import tkinter as tk
import time
import os
import random
import glob
import json
from Gui import Gui
from WindowKeyboard import  WindowKeyboard

class KeyboardTrainer(tk.Tk):
    def __init__(self, user_statistics):
        super().__init__()

        self.user_statistics = user_statistics
        self.gui = Gui(self, user_statistics)
        self.window_keyboard = WindowKeyboard(self)
        self.is_wrong_sequence = False
        self.bind("<F1>", lambda event: self.window_keyboard.open_on_screen_keyboard(event))
        self.windowStats = None
        self.treeStats = None
        self.active_entry = None

    def load_random_text(self, random_choice=True):
        if random_choice:
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

    def populate_text_list(self):
        self.text_choice_listbox.delete(0, tk.END)
        self.text_files = glob.glob("text/*.txt")
        for file_path in self.text_files:
            file_name = os.path.basename(file_path)
            self.text_choice_listbox.insert(tk.END, file_name)

    def set_text(self):
        selected_index = self.text_choice_listbox.curselection()
        if selected_index:
            file_path = self.text_files[selected_index[0]]
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_to_type = file.read().strip()
            self.label_text.configure(state='normal')
            self.label_text.delete('1.0', tk.END)
            self.label_text.insert(tk.END, self.text_to_type)
            self.label_text.configure(state='disabled')
            self.gui.switch_to_trainer_frame()

    def count_texts(self):
        if self.treeStats and self.treeStats.winfo_exists():
            self.treeStats.destroy()
            self.treeStats = None
            self.windowStats.destroy()
            self.windowStats = None

        users_texts = {}
        with open("users.json", 'r') as f:
            data = json.load(f)["users"]
            for user in data:
                users_texts[user["username"]] = user["texts_typed"]
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.gui.display_results_texsts(sorted_users)


    def avarage_speed_print(self):
        if self.treeStats and self.treeStats.winfo_exists():
            self.treeStats.destroy()
            self.treeStats = None
            self.windowStats.destroy()
            self.windowStats = None

        users_texts = {}
        with open("users.json", 'r') as f:
            data = json.load(f)["users"]
            for user in data:
                if user["texts_typed"] == 0:
                    users_texts[user["username"]] = 0
                else:
                    users_texts[user["username"]] = user['total_speed'] / user["texts_typed"]
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.gui.display_avarage_results_speed(sorted_users)

    def max_speed_print(self):
        if self.treeStats and self.treeStats.winfo_exists():
            self.treeStats.destroy()
            self.treeStats = None
            self.windowStats.destroy()
            self.windowStats = None

        users_texts = {}
        with open("users.json", 'r') as f:
            data = json.load(f)["users"]
            for user in data:
                if len(user['training_history']) > 0:
                    average_speed = max(x for x in user['training_history'][0])
                else:
                    average_speed = 0
                users_texts[user["username"]] = average_speed
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.gui.display_max_results_speed(sorted_users)



    def count_mistakes(self):
        if self.treeStats and self.treeStats.winfo_exists():
            self.treeStats.destroy()
            self.treeStats = None
            self.windowStats.destroy()
            self.windowStats = None

        users_texts = {}
        with open("users.json", 'r') as f:
            data = json.load(f)["users"]
            for user in data:
                mistakes_by_char = sum(user['mistakes_by_char'].values())
                users_texts[user['username']] = mistakes_by_char
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=False)
        self.gui.display_count_mistakes(sorted_users)

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
        self.current_position = 0
        self.load_random_text()

    def update_stats_label(self):
        avg_speed = self.user_statistics.get_avg_speed()
        avg_speed_rounded = round(avg_speed, 2)
        self.user_statistics.save_to_file()
        self.label_result.config(text=f"Средняя скорость: {avg_speed_rounded} зн/мин. Ошибок: "
             f"{self.user_statistics.training_history[-1][1] if len(self.user_statistics.training_history) > 0 else 0}",
             foreground="green")


    def update_stats_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        spam = []
        for day, speed in self.user_statistics.speed_dynamics.items():
            spam.append((day, round(speed[0], 2)))
            spam.sort()
        for i in spam:
            self.tree.insert("", "end", values=(i[0], i[1]))