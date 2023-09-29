import tkinter as tk
from tkinter import ttk

from UserStats import UserStatistics


class Gui:
    def __init__(self, kt, user_statistics):
        self.kt = kt
        self.user_statistics = user_statistics
        kt.title("Клавиатурный тренажер")
        kt.geometry("1600x800")
        self.init_ui()

    def init_ui(self):
        self.kt.frames = {}

        self.kt.name_frame = tk.Frame(self.kt)
        self.kt.frames["NameFrame"] = self.kt.name_frame
        self.kt.frames["NameFrame"].pack(fill="both", expand=True)

        self.kt.entry_name = ttk.Entry(self.kt.name_frame, font=("Arial", 14))
        self.kt.entry_name.bind("<FocusIn>", self.track_active_entry)
        self.kt.entry_name.pack(pady=10)
        self.kt.entry_name.insert(0, self.user_statistics.username)
        self.kt.entry_name_button = ttk.Button(self.kt.name_frame, text="Продолжить", command=self.switch_to_trainer_frame)
        self.kt.entry_name_button.pack(pady=5)

        self.kt.trainer_frame = tk.Frame(self.kt)
        self.kt.frames["TrainerFrame"] = self.kt.trainer_frame

        self.kt.label_username = ttk.Label(self.kt.trainer_frame, text=f"Пользователь: {self.user_statistics.username}",
                                        font=("Arial", 14))
        self.kt.label_username.pack(pady=10)

        self.init_trainer_widgets()

        self.kt.stats_frame = tk.Frame(self.kt)
        self.kt.frames["StatsFrame"] = self.kt.stats_frame

        self.kt.text_choice_button_main = ttk.Button(self.kt.trainer_frame,
                                                  text="Выбор текста", command=self.switch_to_text_choice_frame)
        self.kt.text_choice_button_main.pack(pady=5)

        self.kt.tree = ttk.Treeview(self.kt.stats_frame, columns=("char", "count"), show="headings", height=10)
        self.kt.tree.column("char", width=300, anchor="center")
        self.kt.tree.column("count", width=300, anchor="center")
        self.kt.tree.heading("char", text="Символ")
        self.kt.tree.heading("count", text="Ошибок")
        self.kt.tree.pack()

        self.kt.switch_frame_button = ttk.Button(self.kt.stats_frame, text="Вернуться к тренировке",
                                              command=self.switch_to_trainer_frame)
        self.kt.switch_frame_button.pack(pady=5)

        self.kt.text_choice_frame = tk.Frame(self.kt)
        self.kt.frames["TextChoiceFrame"] = self.kt.text_choice_frame

        self.kt.text_choice_label = ttk.Label(self.kt.text_choice_frame, text="Выберите текст для печати:",
                                           font=("Arial", 14))
        self.kt.text_choice_label.pack(pady=10)

        self.kt.text_choice_listbox = tk.Listbox(self.kt.text_choice_frame, font=("Arial", 14), height=10, width=50)
        self.kt.text_choice_listbox.pack(pady=5)

        self.kt.text_choice_button = ttk.Button(self.kt.text_choice_frame, text="Выбрать текст", command=self.kt.set_text)
        self.kt.text_choice_button.pack(pady=5)

        self.kt.text_choice_back_button = ttk.Button(self.kt.text_choice_frame, text="Вернуться к тренировке",
                                                  command=self.switch_to_trainer_frame)
        self.kt.text_choice_back_button.pack(pady=5)

        self.kt.text_choice_button = ttk.Button(self.kt.stats_frame, text="Статистика по количесту текстов",
                                             command=self.kt.count_texts)
        self.kt.text_choice_button.pack(pady=5)

        self.kt.text_choice_button = ttk.Button(self.kt.stats_frame, text="Статистика по средней скорости печати",
                                             command=self.kt.avarage_speed_print)
        self.kt.text_choice_button.pack(pady=5)

        self.kt.text_choice_button = ttk.Button(self.kt.stats_frame, text="Статистика по максимальной скорости печати",
                                             command=self.kt.max_speed_print)
        self.kt.text_choice_button.pack(pady=5)

        self.kt.text_choice_button = ttk.Button(self.kt.stats_frame, text="Статистика по ошибкам",
                                             command=self.kt.count_mistakes)
        self.kt.text_choice_button.pack(pady=5)

    def init_trainer_widgets(self):
        self.kt.current_position = 0
        self.kt.start_time = None
        self.kt.mistakes = 0

        self.kt.entry_var = tk.StringVar()
        self.kt.entry_var.trace("w", self.kt.check_text)

        self.kt.label_text = tk.Text(self.kt.trainer_frame, font=("Arial", 20), height=10, width=50, wrap="word")
        self.kt.label_text.configure(state='disabled')
        self.kt.label_text.tag_configure("green", foreground="green")
        self.kt.label_text.tag_configure("yellow", background="yellow")
        self.kt.label_text.tag_configure("red", foreground="red")
        self.kt.label_text.pack(pady=20)

        self.kt.entry_text = ttk.Entry(self.kt.trainer_frame, textvariable=self.kt.entry_var, font=("Arial", 20))
        self.kt.entry_text.bind("<FocusIn>", self.track_active_entry)
        self.kt.entry_text.pack()

        self.kt.label_result = ttk.Label(self.kt.trainer_frame, text="", font=("Arial", 14))
        self.kt.label_result.pack(pady=20)
        self.kt.switch_frame_button = ttk.Button(self.kt.trainer_frame, text="Сменить пользователя",
                                              command=self.switch_to_name_frame)
        self.kt.switch_frame_button.pack(pady=5)
        self.kt.stats_button = ttk.Button(self.kt.trainer_frame, text="Статистика", command=self.switch_to_stats_frame)
        self.kt.stats_button.pack(pady=5)

        self.kt.load_random_text()

    def switch_to_text_choice_frame(self):
        self.kt.frames["TrainerFrame"].pack_forget()
        self.kt.frames["TextChoiceFrame"].pack(fill="both", expand=True)
        self.kt.populate_text_list()

    def switch_to_trainer_frame(self):
        self.kt.update_username()
        filename = f"{self.user_statistics.username}.json"
        if self.user_statistics.load_from_file(self.user_statistics.username) == 0:
            self.user_statistics = UserStatistics(self.kt.entry_name.get())  # create a new UserStatistics object
            self.user_statistics.save_to_file()  # save the new UserStatistics object to the file
        self.kt.frames["TextChoiceFrame"].pack_forget()
        self.kt.frames["NameFrame"].pack_forget()
        self.kt.frames["StatsFrame"].pack_forget()
        self.kt.frames["TrainerFrame"].pack(fill="both", expand=True)
        self.kt.update_stats_label()

    def switch_to_name_frame(self):
        self.kt.frames["TrainerFrame"].pack_forget()
        self.kt.frames["NameFrame"].pack(fill="both", expand=True)
        self.kt.update_stats_label()

    def switch_to_stats_frame(self):
        self.kt.frames["TrainerFrame"].pack_forget()
        self.kt.frames["StatsFrame"].pack(fill="both", expand=True)
        self.kt.update_stats_table()

    def track_active_entry(self, event):
        self.kt.active_entry = event.widget

    def display_results_texsts(self, sorted_users):
        self.kt.windowStats = tk.Tk()
        self.kt.windowStats.title("Топ пользователей")

        self.kt.treeStats = ttk.Treeview(self.kt.windowStats, columns=("Пользователь", "Количество текстов"), show="headings")
        self.kt.treeStats.heading("Пользователь", text="Пользователь")
        self.kt.treeStats.heading("Количество текстов", text="Количество текстов")
        self.kt.treeStats.pack()

        for i, (user, texts_count) in enumerate(sorted_users[:10]):
            self.kt.treeStats.insert("", i, values=(user, texts_count))

        self.kt.windowStats.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.kt.windowStats.mainloop()

    def display_avarage_results_speed(self, sorted_users):
        self.kt.windowStats = tk.Tk()
        self.kt.windowStats.title("Топ пользователей")
        self.kt.treeStats = ttk.Treeview(self.kt.windowStats, columns=("Пользователь", "Средняя скорость печати"), show="headings")
        self.kt.treeStats.heading("Пользователь", text="Пользователь")
        self.kt.treeStats.heading("Средняя скорость печати", text="Средняя скорость печати")
        self.kt.treeStats.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            self.kt.treeStats.insert("", i, values=(user, round(speed,1)))

        self.kt.windowStats.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.kt.windowStats.mainloop()

    def display_max_results_speed(self, sorted_users):
        self.kt.windowStats = tk.Tk()
        self.kt.windowStats.title("Топ пользователей")

        self.kt.treeStats = ttk.Treeview(self.kt.windowStats, columns=("Пользователь", "Максимальная скорость печати"), show="headings")
        self.kt.treeStats.heading("Пользователь", text="Пользователь")
        self.kt.treeStats.heading("Максимальная скорость печати", text="Максимальная скорость печати")
        self.kt.treeStats.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            self.kt.treeStats.insert("", i, values=(user, round(speed, 1)))

        self.kt.windowStats.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.kt.windowStats.mainloop()

    def display_count_mistakes(self, sorted_users):
        self.kt.windowStats = tk.Tk()
        self.kt.windowStats.title("Топ пользователей")

        self.kt.treeStats = ttk.Treeview(self.kt.windowStats, columns=("Пользователь", "Количество ошибок"), show="headings")
        self.kt.treeStats.heading("Пользователь", text="Пользователь")
        self.kt.treeStats.heading("Количество ошибок", text="Количество ошибок")
        self.kt.treeStats.pack()

        for i, (user, speed) in enumerate(sorted_users[:10]):
            self.kt.treeStats.insert("", i, values=(user, round(speed, 1)))

        self.kt.windowStats.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.kt.windowStats.mainloop()

    def on_window_close(self):
        if self.kt.treeStats and self.kt.treeStats.winfo_exists():
            self.kt.treeStats.destroy()
            self.kt.treeStats = None
        self.kt.windowStats.destroy()
        self.kt.windowStats = None