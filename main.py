import telebot
from telebot import types
import random
import os
import re

user_token = "6080459375:AAHCWM8yvoYYjcVTNby5sLpK4UJxWy4wSCI"
user_images_folder = r"C:\Users\nsrod\Pictures\images"
user_images_folder = re.sub(r'\\', '/', user_images_folder)
user_sounds_folder = r"C:\Users\nsrod\Music\sounds"
user_sounds_folder = re.sub(r'\\', '/', user_sounds_folder)


class Bot:
    def __init__(self, token, images_folder, sounds_folder):
        self.bot = telebot.TeleBot(token)
        self.images_folder = images_folder
        self.sounds_folder = sounds_folder

    def start(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            keyboard = types.ReplyKeyboardMarkup(True)
            keyboard.add('Дай звук')
            self.bot.send_message(
                text="Привет! Я ваш бот. Как я могу помочь?",
                chat_id=message.chat.id,
                reply_markup=keyboard
            )

        @self.bot.message_handler(func=lambda message: "изображение" in message.text.lower())
        def send_random_image(message):
            # Получение списка файлов из папки с изображениями
            image_files = [f for f in os.listdir(self.images_folder) if
                           os.path.isfile(os.path.join(self.images_folder, f))]

            if image_files:
                # Выбор случайного изображения из списка
                random_image = random.choice(image_files)
                # Полный путь к выбранному изображению
                image_path = os.path.join(self.images_folder, random_image)

                # Отправка изображения пользователю
                with open(image_path, 'rb') as image_file:
                    self.bot.send_photo(message.chat.id, image_file)

        @self.bot.message_handler(func=lambda message: "звук" in message.text.lower())
        def send_random_sound(message):
            sound_files = [f for f in os.listdir(self.sounds_folder)
                           if os.path.isfile(os.path.join(self.sounds_folder, f))]
            if sound_files:
                random_sound = random.choice(sound_files)
                sound_path = os.path.join(self.sounds_folder, random_sound)

                with open(sound_path, 'rb') as sound_file:
                    self.bot.send_voice(message.chat.id, sound_file)

        self.bot.polling(none_stop=True)


if __name__ == "__main__":
    my_bot = Bot(user_token, user_images_folder, user_sounds_folder)
    my_bot.start()
