import telebot
from config import TOKEN
from db import create_tables
from register import register_user

bot = telebot.TeleBot(TOKEN)

if __name__ == "__main__":
    create_tables()
    register_user(bot)
    bot.infinity_polling()

