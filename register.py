from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

user_data = {}


def register_user(bot):
    @bot.message_handler(commands=['start'])
    def ask_name(message: Message):
        bot.send_message(message.chat.id, "Iltimos, ismingizni kiriting:")
        bot.register_next_step_handler(message, get_name)

    def get_name(message: Message):
        user_data[message.chat.id] = {'full_name': message.text}

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        phone_button = KeyboardButton("📞 Raqamni yuborish", request_contact=True)
        markup.add(phone_button)

        bot.send_message(message.chat.id, "Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)
        bot.register_next_step_handler(message, get_phone)

    @bot.message_handler(content_types=['contact'])
    def get_phone(message: Message):
        contact = message.contact
        chat_id = message.chat.id
        if chat_id in user_data:
            full_name = user_data[chat_id]['full_name']
            phone_number = contact.phone_number
            add_user(message.from_user.id, full_name, phone_number)
            bot.send_message(chat_id, f"Rahmat, {full_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz ✅")
        else:
            bot.send_message(chat_id, "Avval ismingizni kiriting. /start buyrug'ini bosing.")

