'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import registration, send_contact
from keyboards.inline import get_categories_buttons


@bot.message_handler(func=lambda message: message.text == "Katalog 📇")
def catalog(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    check = db.check_user_for_registration(from_user_id)
    if None in check:
        text = '''Siz ro'yxatdan o'tmagansiz. Iltimos ro'yxatdan o'ting'''
        markup = registration()
    else:
        # bot.delete_message(chat_id, message.message_id)
        text = '''Katalog'''
        bot.send_message(chat_id, "Siz buni ko'rishingiz kerak mas edi", reply_markup=ReplyKeyboardRemove())
        bot.delete_message(chat_id, message.message_id + 1)
        categories_list = db.select_all_categories()
        markup = get_categories_buttons(categories_list)

    bot.send_message(chat_id, text, reply_markup=markup)



data = {}

@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish 📝")
def register(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    msg = bot.send_message(chat_id, "Ism va familiyangizni kiriting!\n"
                                    "Namuna 👇\n\n"
                                    "Falonchiyev Falonchi", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, save_name)

def save_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    full_name = message.text.title()

    data[from_user_id] = {'full_name': full_name}

    msg = bot.send_message(chat_id, "Telefon nomeringizni kiriting!", reply_markup=send_contact())
    bot.register_next_step_handler(msg, contact_save)

def contact_save(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    contact = message.contact.phone_number

    data[from_user_id]['contact'] = contact

    msg = bot.send_message(chat_id, "Tug'ilgan kuningizni <b>yyyy.mm.dd</b> ko'rinishida kiriting: ",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, user_save)

def user_save(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    birth_date = message.text
    data[from_user_id]['birth_date'] = birth_date
    full_name = data[from_user_id]['full_name']
    contact = data[from_user_id]['contact']
    db.save_user(full_name, contact, birth_date, from_user_id)

    categories_list = db.select_all_categories()

    bot.send_message(chat_id, "Ro'yxatdan o'tdingiz", reply_markup=get_categories_buttons(categories_list))
