from .BaseHandler import BaseHandler
from telebot import types


class StartHandler(BaseHandler):
    def handle(self, message):
        self.main_menu(message)

    def main_menu(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Заказать справку', 'Узнать перечень документов на замену паспорта', 'Получить информацию о работе паспортных столов г. Гомель']
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(message.chat.id, f"Добрый день, {message.from_user.first_name}! Чем я могу вам помочь?", reply_markup=markup)
