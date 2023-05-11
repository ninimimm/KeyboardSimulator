import tkinter as tk
from tkinter import ttk
import time
import os
import random
import glob
import json
import UserStats as UserStatistics

class KeyboardTrainer(tk.Tk):
    def __init__(self, user_statistics):
        super().__init__()

        self.title("Клавиатурный тренажер")
        self.geometry("1600x800")
        self.user_statistics = user_statistics
        self.is_wrong_sequence = False
        self.init_ui()

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

        self.text_choice_button_main = ttk.Button(self.trainer_frame, text="Выбор текста", command=self.switch_to_text_choice_frame)
        self.text_choice_button_main.pack(pady=5)


        self.tree = ttk.Treeview(self.stats_frame, columns=("char", "count"), show="headings", height=10)
        self.tree.column("char", width=300, anchor="center")
        self.tree.column("count", width=300, anchor="center")
        self.tree.heading("char", text="Символ")
        self.tree.heading("count", text="Ошибок")
        self.tree.pack()

        self.switch_frame_button = ttk.Button(self.stats_frame, text="Вернуться к тренировке", command=self.switch_to_trainer_frame)
        self.switch_frame_button.pack(pady=5)

        self.text_choice_frame = tk.Frame(self)
        self.frames["TextChoiceFrame"] = self.text_choice_frame

        self.text_choice_label = ttk.Label(self.text_choice_frame, text="Выберите текст для печати:",
                                           font=("Arial", 14))
        self.text_choice_label.pack(pady=10)

        self.text_choice_listbox = tk.Listbox(self.text_choice_frame, font=("Arial", 14), height=10, width=50)
        self.text_choice_listbox.pack(pady=5)

        self.text_choice_button = ttk.Button(self.text_choice_frame, text="Выбрать текст", command=self.set_text)
        self.text_choice_button.pack(pady=5)

        self.text_choice_back_button = ttk.Button(self.text_choice_frame, text="Вернуться к тренировке",
                                                  command=self.switch_to_trainer_frame)
        self.text_choice_back_button.pack(pady=5)

        self.text_choice_button = ttk.Button(self.stats_frame, text="Статистика по количесту текстов",
                                             command=self.count_texts)
        self.text_choice_button.pack(pady=5)

        self.text_choice_button = ttk.Button(self.stats_frame, text="Статистика по средней скорости печати",
                                             command=self.avarage_speed_print)
        self.text_choice_button.pack(pady=5)

        self.text_choice_button = ttk.Button(self.stats_frame, text="Статистика по максимальной скорости печати",
                                             command=self.max_speed_print)
        self.text_choice_button.pack(pady=5)

        self.text_choice_button = ttk.Button(self.stats_frame, text="Статистика по ошибкам",
                                             command=self.count_mistaces)
        self.text_choice_button.pack(pady=5)


    def init_trainer_widgets(self):
        self.current_position = 0
        self.start_time = None
        self.mistakes = 0

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.check_text)

        self.label_text = tk.Text(self.trainer_frame, font=("Arial", 20), height=10, width=50, wrap="word")
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

    def switch_to_text_choice_frame(self):
        self.frames["TrainerFrame"].pack_forget()
        self.frames["TextChoiceFrame"].pack(fill="both", expand=True)
        self.populate_text_list()

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
            self.switch_to_trainer_frame()

    def count_texts(self):
        json_files = [f for f in os.listdir() if f.endswith('.json')]

        users_texts = {}

        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)
                if 'username' in data and 'texts_typed' in data:
                    user = data['username']
                    texts_typed = data['texts_typed']
                    users_texts[user] = texts_typed
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.display_results_texsts(sorted_users)

    def display_results_texsts(self, sorted_users):
        root = tk.Tk()
        root.title("Топ пользователей")

        tree = ttk.Treeview(root, columns=("Пользователь", "Количество текстов"), show="headings")
        tree.heading("Пользователь", text="Пользователь")
        tree.heading("Количество текстов", text="Количество текстов")
        tree.pack()

        for i, (user, texts_count) in enumerate(sorted_users[:10]):
            tree.insert("", i, values=(user, texts_count))


    def avarage_speed_print(self):
        json_files = [f for f in os.listdir() if f.endswith('.json')]

        users_texts = {}

        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)
                if 'username' in data and 'total_speed' in data:
                    user = data['username']
                    average_speed = data['total_speed']/data["texts_typed"]
                    users_texts[user] = average_speed
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.display_avarage_results_speed(sorted_users)

    def display_avarage_results_speed(self, sorted_users):
        root = tk.Tk()
        root.title("Топ пользователей")

        tree = ttk.Treeview(root, columns=("Пользователь", "Средняя скорость печати"), show="headings")
        tree.heading("Пользователь", text="Пользователь")
        tree.heading("Средняя скорость печати", text="Средняя скорость печати")
        tree.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            tree.insert("", i, values=(user, round(speed,1)))

    def max_speed_print(self):
        json_files = [f for f in os.listdir() if f.endswith('.json')]

        users_texts = {}

        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)
                if 'username' in data and 'total_speed' in data:
                    user = data['username']
                    average_speed = max(x for x in data['training_history'][0])
                    users_texts[user] = average_speed
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=True)

        self.display_max_results_speed(sorted_users)

    def display_max_results_speed(self, sorted_users):
        root = tk.Tk()
        root.title("Топ пользователей")

        tree = ttk.Treeview(root, columns=("Пользователь", "Максимальная скорость печати"), show="headings")
        tree.heading("Пользователь", text="Пользователь")
        tree.heading("Максимальная скорость печати", text="Максимальная скорость печати")
        tree.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            tree.insert("", i, values=(user, round(speed,1)))


    def count_mistaces(self):
        json_files = [f for f in os.listdir() if f.endswith('.json')]

        users_texts = {}

        for file in json_files:
            with open(file, 'r') as f:
                data = json.load(f)
                if 'username' in data and 'mistakes_by_char' in data:
                    user = data['username']
                    texts_typed = sum(data['mistakes_by_char'].values())
                    users_texts[user] = texts_typed
        sorted_users = sorted(users_texts.items(), key=lambda x: x[1], reverse=False)

        self.display_count_mistaces(sorted_users)

    def display_count_mistaces(self, sorted_users):
        root = tk.Tk()
        root.title("Топ пользователей")

        tree = ttk.Treeview(root, columns=("Пользователь", "Количество ошибок"), show="headings")
        tree.heading("Пользователь", text="Пользователь")
        tree.heading("Количество ошибок", text="Количество ошибок")
        tree.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            tree.insert("", i, values=(user, round(speed,1)))

    def switch_to_trainer_frame(self):
        self.update_username()
        filename = f"{self.user_statistics.username}.json"
        existing_user_stats = UserStatistics.UserStatistics.load_from_file(filename)
        if existing_user_stats:
            self.user_statistics = existing_user_stats
        else:
            self.user_statistics = UserStatistics.UserStatistics(self.entry_name.get())  # create a new UserStatistics object
            self.user_statistics.save_to_file(filename)  # save the new UserStatistics object to the file
        self.frames["TextChoiceFrame"].pack_forget()
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
        self.current_position = 0
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