import json
import unittest
import os
import glob
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
from KeyboardTrainer import KeyboardTrainer
from UserStats import UserStatistics

class TestKeyboardTrainer(unittest.TestCase):
    def setUp(self):
        self.user_stats = Mock()
        self.kt = KeyboardTrainer(self.user_stats)

    @patch('glob.glob')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="test text")
    def test_load_random_text(self, mock_open, mock_glob):
        mock_glob.return_value = ['text/test.txt']
        self.kt.load_random_text()

        mock_glob.assert_called_once_with('text/*.txt')
        mock_open.assert_called_once_with('text/test.txt', 'r', encoding='utf-8')
        self.assertEqual(self.kt.text_to_type, "test text")
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

    def test_init_ui(self):
        self.kt.init_ui()

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
        # And so on for every widget you want to test

    def test_init_trainer_widgets(self):
        self.kt.init_ui()  # We need to call this first to set up the trainer_frame
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

    @patch('tkinter.Tk')
    @patch('tkinter.ttk.Treeview')
    def test_display_results_texts(self, mock_treeview, mock_tk):
        self.kt.display_results_texsts([('test_user', 5)])

        mock_treeview.assert_called_once_with(self.kt.windowStats, columns=("Пользователь", "Количество текстов"), show="headings")
        self.kt.treeStats.heading.assert_any_call("Пользователь", text="Пользователь")
        self.kt.treeStats.heading.assert_any_call("Количество текстов", text="Количество текстов")
        self.kt.treeStats.pack.assert_called_once()
        self.kt.treeStats.insert.assert_called_once_with("", 0, values=('test_user', 5))
        self.kt.windowStats.protocol.assert_called_once_with("WM_DELETE_WINDOW", self.kt.on_window_close)
        self.kt.windowStats.mainloop.assert_called_once()

if __name__ == '__main__':
    unittest.main()

