from KeyboardTrainer import KeyboardTrainer
from UserStats import UserStatistics

if __name__ == "__main__":
    user_stats = UserStatistics("Базовый пользователь")
    app = KeyboardTrainer(user_stats)
    app.mainloop()
