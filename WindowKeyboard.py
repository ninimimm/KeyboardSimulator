import tkinter as tk

class WindowKeyboard:
    def __init__(self, kt):
        self.kt = kt
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '0', '<<'],
            ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з'],
            ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж'],
            ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.'],
            ['!', '?', ',', ':', ';', '-', '(', ')', '@', '#'],
        ]

    def open_on_screen_keyboard(self, event=None):
        if hasattr(self, 'keyboard_window') and self.keyboard_window.winfo_exists():
            self.keyboard_window.destroy()
            return

        shift_pressed = tk.BooleanVar(self.kt, False)

        def select(value):
            if self.kt.active_entry:
                if value == "<<":
                    if self.kt.active_entry.get():
                        self.kt.active_entry.delete(self.kt.active_entry.index('end') - 1, 'end')
                elif value == " Пробел ":
                    self.kt.active_entry.insert('insert', ' ')
                else:
                    if shift_pressed.get():
                        self.kt.active_entry.insert('insert', value.upper())
                    else:
                        self.kt.active_entry.insert('insert', value.lower())


        keyboard_window = tk.Toplevel(self.kt)

        for y, row in enumerate(self.keys, 1):
            for x, key in enumerate(row):
                button = tk.Button(keyboard_window, text=key, command=lambda value=key: select(value))
                button.grid(row=y+1, column=x+1)

        shift_frame = tk.Frame(keyboard_window)
        shift_button = tk.Checkbutton(shift_frame, text="Shift", variable=shift_pressed)
        shift_button.pack(fill=tk.BOTH, expand=True)
        shift_frame.grid(row=5, column=0)

        space_frame = tk.Frame(keyboard_window)
        space_button = tk.Button(space_frame, text=" Пробел ", command=lambda value=" Пробел ": select(value))
        space_button.pack(fill=tk.BOTH, expand=True)
        space_frame.grid(row=7, column=2, columnspan=8)

        self.kt.keyboard_window = keyboard_window