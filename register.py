from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from db import add_user, is_user_registered

user_data = {}

def register_user(bot):
    @bot.message_handler(commands=['start'])
    def ask_name(message: Message):
        chat_id = message.chat.id
        telegram_id = message.from_user.id

        if is_user_registered(telegram_id):
            bot.send_message(chat_id, "✅ Siz allaqachon ro'yxatdan o'tgansiz.")
        else:
            bot.send_message(chat_id, "Iltimos, ismingizni kiriting:")
            bot.register_next_step_handler(message, get_name)

    def get_name(message: Message):
        chat_id = message.chat.id
        full_name = message.text
        user_data[chat_id] = {'full_name': full_name}

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        phone_button = KeyboardButton("📞 Raqamni yuborish", request_contact=True)
        markup.add(phone_button)

        bot.send_message(chat_id, "Endi telefon raqamingizni yuboring:", reply_markup=markup)

    @bot.message_handler(content_types=['contact'])
    def get_phone(message: Message):
        chat_id = message.chat.id
        contact = message.contact
        telegram_id = message.from_user.id

        if chat_id in user_data:
            full_name = user_data[chat_id]['full_name']
            phone_number = contact.phone_number

            add_user(telegram_id, full_name, phone_number)
            bot.send_message(chat_id, f"✅ Rahmat, {full_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
        else:
            bot.send_message(chat_id, "Avval ismingizni kiriting. /start buyrug'ini bosing.")
