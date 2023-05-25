import json
import time
import unittest
import os
import glob
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
from KeyboardTrainer import KeyboardTrainer
from UserStats import UserStatistics
from tkinter import Entry, Label
from tkinter.ttk import Treeview
class CustomMock(Mock):
    def __round__(self, n=0):
        return round(n)

class MockEvent:
    def __init__(self, widget):
        self.widget = widget

class MockKeyboardWindow:
    def __init__(self):
        self.destroy_called = False

    def destroy(self):
        self.destroy_called = True

class TestKeyboardTrainer(unittest.TestCase):
    def setUp(self):
        self.user_stats = CustomMock(spec=UserStatistics)
        self.kt = KeyboardTrainer(self.user_stats)
        self.kt.label_result = tk.Label()

    def tearDown(self):
        self.kt = None

    @patch('glob.glob')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test text")
    def test_load_random_text(self, mock_open, mock_glob):
        mock_glob.return_value = ['text/test.txt']
        self.kt.load_random_text()

        mock_glob.assert_called_once_with('text/*.txt')
        mock_open.assert_called_once_with('text/test.txt', 'r', encoding='utf-8')
        self.assertEqual(self.kt.text_to_type, "test text")
        self.assertNotEqual(self.kt.text_to_type, "No text files found in the 'text' folder.")
        self.assertEqual(self.kt.label_text.get("1.0", "end-1c"), "test text")

    @patch('glob.glob')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test text")
    def test_load_random_text_no_files(self, mock_open, mock_glob):
        mock_glob.return_value = []
        self.kt.load_random_text()

        mock_glob.assert_called_once_with('text/*.txt')
        mock_open.assert_not_called()
        self.assertEqual(self.kt.text_to_type, "No text files found in the 'text' folder.")
        self.assertEqual(self.kt.label_text.get("1.0", "end-1c"), "No text files found in the 'text' folder.")

    def check_ui_initialization(self):
        self.assertTrue(self.kt.frames)
        self.assertTrue(self.kt.name_frame)
        self.assertTrue(self.kt.entry_name)
        self.assertTrue(self.kt.entry_name_button)
        self.assertTrue(self.kt.trainer_frame)
        self.assertTrue(self.kt.label_username)
        self.assertTrue(self.kt.stats_frame)
        self.assertTrue(self.kt.text_choice_button_main)
        self.assertTrue(self.kt.tree)
        self.assertTrue(self.kt.switch_frame_button)
        self.assertTrue(self.kt.text_choice_frame)
        self.assertTrue(self.kt.text_choice_label)
        self.assertTrue(self.kt.text_choice_listbox)
        self.assertTrue(self.kt.text_choice_button)
        self.assertTrue(self.kt.text_choice_back_button)

    def test_init_ui(self):
        self.kt.init_ui()
        self.check_ui_initialization()

    def test_init_trainer_widgets(self):
        self.kt.init_ui()
        self.kt.init_trainer_widgets()

        self.assertEqual(self.kt.current_position, 0)
        self.assertIsNone(self.kt.start_time)
        self.assertEqual(self.kt.mistakes, 0)
        self.assertTrue(self.kt.entry_var)
        self.assertTrue(self.kt.label_text)
        self.assertTrue(self.kt.entry_text)
        self.assertTrue(self.kt.label_result)
        self.assertTrue(self.kt.switch_frame_button)
        self.assertTrue(self.kt.stats_button)

        self.check_ui_initialization()

    @patch('tkinter.Tk')
    @patch('tkinter.ttk.Treeview')
    def test_display_results_texts(self, mock_treeview, mock_tk):
        self.kt.display_results_texsts([('test_user', 5)])

        mock_treeview.assert_called_once_with(self.kt.windowStats, columns=("Пользователь", "Количество текстов"),
                                              show="headings")
        self.kt.treeStats.heading.assert_any_call("Пользователь", text="Пользователь")
        self.kt.treeStats.heading.assert_any_call("Количество текстов", text="Количество текстов")
        self.kt.treeStats.pack.assert_called_once()
        self.kt.treeStats.insert.assert_called_once_with("", 0, values=('test_user', 5))
        self.kt.windowStats.protocol.assert_called_once_with("WM_DELETE_WINDOW", self.kt.on_window_close)
        self.kt.windowStats.mainloop.assert_called_once()

    @patch('glob.glob')
    @patch.object(tk.Listbox, 'insert')
    def test_populate_text_list(self, mock_insert, mock_glob):
        mock_glob.return_value = ['text/test1.txt', 'text/test2.txt', 'text/test3.txt']
        self.kt.populate_text_list()

        mock_glob.assert_called_with('text/*.txt')
        self.assertEqual(self.kt.text_files, ['text/test1.txt', 'text/test2.txt', 'text/test3.txt'])
        mock_insert.assert_any_call(tk.END, 'test1.txt')
        mock_insert.assert_any_call(tk.END, 'test2.txt')
        mock_insert.assert_any_call(tk.END, 'test3.txt')

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test text")
    @patch.object(tk.Listbox, 'curselection')
    def test_set_text(self, mock_curselection, mock_open):
        self.kt.text_files = ['text/test1.txt', 'text/test2.txt', 'text/test3.txt']
        mock_curselection.return_value = (1,)
        self.kt.set_text()

        mock_open.assert_any_call('text/test2.txt', 'r', encoding='utf-8')
        self.assertEqual(self.kt.text_to_type, "test text")
        self.assertEqual(self.kt.label_text.get("1.0", "end-1c"), "test text")

    def test_check_text_correct_input(self):
        self.kt.entry_var.set("test")
        self.kt.text_to_type = "test"
        self.kt.current_position = 0
        self.kt.start_time = None
        self.kt.mistakes = 0
        self.kt.is_wrong_sequence = False

        self.kt.check_text()

        self.assertEqual(self.kt.current_position, 0)
        self.assertEqual(self.kt.label_result.cget("text"), "Скорость: 0.00 зн/мин. Опечатки: 0")
        self.assertEqual(self.kt.label_result.cget("foreground"), "green")
    def test_check_text_incorrect_input(self):
        self.kt.entry_var.set("wrong")
        self.kt.text_to_type = "correct"
        self.kt.current_position = 0
        self.kt.start_time = None
        self.kt.mistakes = 0
        self.kt.is_wrong_sequence = False

        self.kt.check_text()

        self.assertEqual(self.kt.current_position, 0)
        self.assertIsNone(self.kt.start_time)
        self.assertEqual(self.kt.mistakes, 1)
        self.assertEqual(self.kt.label_result.cget("text"), "Ошибка! Исправьте ошибку и продолжайте.")
        self.assertEqual(self.kt.label_result.cget("foreground"), "red")

    def test_reset(self):
        self.kt.entry_text = Entry()
        self.kt.start_time = 12345
        self.kt.mistakes = 5
        self.kt.current_position = 10

        self.kt.reset()

        self.assertEqual(self.kt.entry_text.get(), '')
        self.assertIsNone(self.kt.start_time)
        self.assertEqual(self.kt.mistakes, 0)
        self.assertEqual(self.kt.current_position, 0)

    def test_update_stats_label(self):
        self.kt.user_statistics = UserStatistics(username="test_user")
        self.kt.user_statistics.add_result(50, 3)
        self.kt.mistakes = 3
        self.kt.label_result = Label()

        self.kt.update_stats_label()

        self.assertEqual(self.kt.label_result.cget('text'), 'Средняя скорость: 50.0 зн/мин. Ошибок: 3')
        self.assertEqual(self.kt.label_result.cget('foreground'), 'green')

    def test_update_stats_table(self):
        self.kt.user_statistics = UserStatistics(username="test_user")
        self.kt.user_statistics.add_result(60, 2)
        self.kt.user_statistics.add_result(70, 1)
        self.kt.user_statistics.add_result(55, 4)
        self.kt.tree = MagicMock()

        self.kt.update_stats_table()

        items = self.kt.tree.get_children()
        values = [self.kt.tree.item(item)['values'] for item in items]

        expected_values = [('Day 1', 60.0), ('Day 2', 70.0), ('Day 3', 55.0)]

        self.assertEqual(len(items), len(expected_values))
        self.assertEqual(values, expected_values)

    def test_track_active_entry(self):
        self.kt.active_entry = None
        event = MockEvent(widget=Entry())

        self.kt.track_active_entry(event)

        self.assertEqual(self.kt.active_entry, event.widget)

    def test_open_on_screen_keyboard_keyboard_exists(self):
        self.kt.keyboard_window = MockKeyboardWindow(winfo_exists=True)

        self.kt.open_on_screen_keyboard()

        self.assertTrue(self.kt.keyboard_window.destroy_called)

    def test_open_on_screen_keyboard_keyboard_not_exists(self):
        self.kt.keyboard_window = MockKeyboardWindow(winfo_exists=False)

        self.kt.open_on_screen_keyboard()

        self.assertIsNotNone(self.kt.keyboard_window)

class MockEvent:
    def __init__(self, widget):
        self.widget = widget

class MockKeyboardWindow:
    def __init__(self, winfo_exists):
        self.destroy_called = False
        self.winfo_exists_val = winfo_exists

    def winfo_exists(self):
        return self.winfo_exists_val

    def destroy(self):
        self.destroy_called = True

if __name__ == '__main__':
    unittest.main()
