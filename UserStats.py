import json
import os
import datetime


class UserStatistics:
    def __init__(self, username):
        self.username = username
        self.texts_typed = 0
        self.total_speed = 0
        self.training_history = []
        self.mistakes_by_char = {}
        self.speed_dynamics = {}

    def add_result(self, speed, mistakes):
        self.texts_typed += 1
        self.total_speed += speed
        self.training_history.append((speed, mistakes))
        day = str(datetime.date.today())
        if day not in self.speed_dynamics:
            self.speed_dynamics[day] = [speed, 1]
        else:
            eggs = self.speed_dynamics[day][0] * self.speed_dynamics[day][1]
            eggs += speed
            self.speed_dynamics[day][1] += 1
            self.speed_dynamics[day][0] = eggs / self.speed_dynamics[day][1]

    def add_mistake(self, mistake_char):
        if mistake_char not in self.mistakes_by_char:
            self.mistakes_by_char[mistake_char] = 1
        else:
            self.mistakes_by_char[mistake_char] += 1
        dict(sorted(self.mistakes_by_char.items(), key=lambda item: item[1]))

    def get_avg_speed(self):
        return self.total_speed / self.texts_typed if self.texts_typed > 0 else 0

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump({
                "username": self.username,
                "texts_typed": self.texts_typed,
                "total_speed": self.total_speed,
                "training_history": self.training_history,
                "mistakes_by_char": self.mistakes_by_char,
                "speed_dynamics": self.speed_dynamics
            }, f)

    def username(self):
        return self.username

    @classmethod
    def load_from_file(cls, filename):
        if not os.path.exists(filename):
            return None

        with open(filename, "r") as f:
            data = json.load(f)

        user_stats = cls(data["username"])
        user_stats.texts_typed = data["texts_typed"]
        user_stats.total_speed = data["total_speed"]
        user_stats.training_history = data["training_history"]
        user_stats.mistakes_by_char = data["mistakes_by_char"]
        user_stats.speed_dynamics = data["speed_dynamics"]
        return user_stats
