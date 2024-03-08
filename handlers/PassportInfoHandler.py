from .BaseHandler import BaseHandler
from telebot import types


class PassportInfoHandler(BaseHandler):
    def handle(self, message):
        self.show_passport_type_choice(message)

    def show_passport_type_choice(self, message):
        # Создаем клавиатуру для выбора типа паспорта
        passport_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        passport_markup.add(
            types.KeyboardButton('Детский паспорт'),
            types.KeyboardButton('Взрослый паспорт'),
            types.KeyboardButton('Вернуться назад')
        )
        self.bot.send_message(message.chat.id, "Выберите тип паспорта:", reply_markup=passport_markup)
        self.bot.register_next_step_handler(message, self.passport_type)

    def passport_type(self, message):
        # Обрабатываем выбор пользователя
        if message.text == 'Детский паспорт':
            self.show_child_passport_info(message)
        elif message.text == 'Взрослый паспорт':
            self.show_adult_passport_info(message)
        elif message.text == 'Вернуться назад':
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        else:
            self.handle_unknown(message, self.show_passport_type_choice)

    def show_child_passport_info(self, message):
        # Показываем информацию о документах для детского паспорта
        response = ("👶 *Свидетельство о рождении:* необходимо предъявить оригинал и копию...\n"
                    "📕 *Старый паспорт:* если ребенку ранее был выдан паспорт...\n"
                    "🖼 *4 фото на паспорт:* фотографии должны быть подписаны с обратной стороны...\n"
                    "🛂 *Паспорт одного из родителей:* в случае оформления первичного паспорта для ребенка, требуется предоставить паспорт одного из родителей.")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def show_adult_passport_info(self, message):
        # Показываем информацию о документах для взрослого паспорта
        response = ("📖 *Документы на паспорт для граждан от 18 лет и старше:*\n"
                    "🖼 4 фото на паспорт: подписанные с обратной стороны (Фамилия, имя, отчество полное)...\n"
                    "📄 Копия свидетельства о рождении: необходимо для подтверждения личности заявителя...\n"
                    "💍 Копия свидетельства о браке или решение суда о разводе: для подтверждения семейного статуса...")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def show_final_choice(self, message):
        # Показываем клавиатуру с выбором "Спасибо за информацию" и "Вернуться назад"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Вернуться назад'), types.KeyboardButton('Спасибо за информацию'))
        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_final_choice)

    def handle_final_choice(self, message):
        # Обрабатываем выбор пользователя после показа информации
        if message.text == 'Вернуться назад':
            self.show_passport_type_choice(message)
        elif message.text == 'Спасибо за информацию':
            self.bot.send_message(message.chat.id, "Рады были помочь! Если у вас есть ещё вопросы, вы всегда можете вернуться в главное меню.")
        else:
            self.handle_unknown(message, self.show_final_choice)
