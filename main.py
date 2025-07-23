import telebot
from config import TOKEN
from db import create_tables, get_books, create_books_table, insert_sample_books
from register import register_user
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


create_tables()
create_books_table()
insert_sample_books()
bot = telebot.TeleBot(TOKEN)

user_offsets = {}

@bot.message_handler(commands=['books'])
def show_books(message):
    chat_id = message.chat.id
    user_offsets[chat_id] = 0
    send_books_list(chat_id, offset=0)

@bot.callback_query_handler(func=lambda call: call.data.startswith("next_"))
def next_books(call):
    chat_id = call.message.chat.id
    offset = int(call.data.split("_")[1])
    user_offsets[chat_id] = offset
    send_books_list(chat_id, offset=offset)

def send_books_list(chat_id, offset):
    books = get_books(limit=10, offset=offset)

    if not books:
        bot.send_message(chat_id, "🚫 Boshqa kitoblar topilmadi.")
        return

    text = ""
    for title, author in books:
        text += f"📚 *{title}* — _{author}_\n"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➡️ Next", callback_data=f"next_{offset + 10}"))

    bot.send_message(chat_id, text, reply_markup=markup)

if __name__ == "__main__":
    create_tables()
    register_user(bot)
    bot.infinity_polling()

