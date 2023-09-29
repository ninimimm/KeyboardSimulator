import json
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

    def save_to_file(self):
        with open("users.json", "r") as file:
            all_user_data = json.load(file)

        flag = True
        for user in all_user_data["users"]:
            if user["username"] == self.username:
                user["texts_typed"] = self.texts_typed
                user["total_speed"] = self.total_speed
                user["training_history"] = self.training_history
                user["mistakes_by_char"] = self.mistakes_by_char
                user["speed_dynamics"] = self.speed_dynamics
                flag = False
                break
        if flag: all_user_data["users"].append({
                "username" : self.username,
                "texts_typed" : 0,
                "total_speed" : 0,
                "training_history" : [],
                "mistakes_by_char" : {},
                "speed_dynamics" : {}
            })


        with open("users.json", "w") as file:
            json.dump(all_user_data, file, indent=4)

    def load_from_file(self, username):
        self.save_to_file()
        with open("users.json", "r") as f:
            data = json.load(f)
        flag = True
        self.username = username
        self.texts_typed = 0
        self.total_speed = 0
        self.training_history = []
        self.mistakes_by_char = {}
        self.speed_dynamics = {}
        for user in data["users"]:
            if user["username"] == username:
                self.texts_typed = user["texts_typed"]
                self.total_speed = user["total_speed"]
                self.training_history = user["training_history"]
                self.mistakes_by_char = user["mistakes_by_char"]
                self.speed_dynamics = user["speed_dynamics"]
                flag = False
                break
        if flag: return 0
        return 1
