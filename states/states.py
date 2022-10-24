from telebot.handler_backends import State, StatesGroup


class CardState(StatesGroup):
    card = State()