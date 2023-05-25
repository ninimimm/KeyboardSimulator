import unittest
import os
from UserStats import UserStatistics


class TestUserStatistics(unittest.TestCase):
    def setUp(self):
        self.user_stats = UserStatistics('TestUser')

    def test_add_result(self):
        self.assertEqual(self.user_stats.texts_typed, 0)
        self.assertEqual(self.user_stats.total_speed, 0)
        self.user_stats.add_result(100, 5)
        self.assertEqual(self.user_stats.texts_typed, 1)
        self.assertEqual(self.user_stats.total_speed, 100)

    def test_add_mistake(self):
        self.assertEqual(self.user_stats.mistakes_by_char, {})
        self.user_stats.add_mistake('a')
        self.assertEqual(self.user_stats.mistakes_by_char, {'a': 1})

    def test_get_avg_speed(self):
        self.assertEqual(self.user_stats.get_avg_speed(), 0)
        self.user_stats.add_result(100, 5)
        self.assertEqual(self.user_stats.get_avg_speed(), 100)

    def test_save_and_load(self):
        filename = "test_user_stats.json"
        self.user_stats.add_result(100, 5)
        self.user_stats.add_mistake('a')
        self.user_stats.save_to_file(filename)

        loaded_user_stats = UserStatistics.load_from_file(filename)
        self.assertEqual(loaded_user_stats.texts_typed, 1)
        self.assertEqual(loaded_user_stats.total_speed, 100)
        self.assertEqual(loaded_user_stats.mistakes_by_char, {'a': 1})
        os.remove(filename)  # Clean up the test file

    def test_username(self):
        self.assertEqual(self.user_stats.username, 'TestUser')

if __name__ == '__main__':
    unittest.main()
