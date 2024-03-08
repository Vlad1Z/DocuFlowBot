from .BaseHandler import BaseHandler
from telebot import types


class PassportOfficeInfoHandler(BaseHandler):
    def handle(self, message):
        """Обработка начального сообщения и показ выбора паспортного стола."""
        self.show_passport_office_choice(message)

    def show_passport_office_choice(self, message):
        """Показывает пользователю кнопки для выбора районного паспортного стола."""
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        districts = [
            'Центрального района Гомеля',
            'Советского района Гомеля',
            'Новобелицкого района Гомеля',
            'Железнодорожного района Гомеля',
            'Вернуться назад'
        ]
        for district in districts:
            markup.add(types.KeyboardButton(district))
        self.bot.send_message(message.chat.id, "Выберите паспортный стол:", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_passport_office_choice)

    def handle_passport_office_choice(self, message):
        """Обрабатывает выбор пользователя по паспортному столу или возврат в главное меню."""
        if message.text == 'Вернуться назад':
            from .StartHandler import StartHandler  # Путь импорта должен быть корректным
            StartHandler(self.bot).handle(message)
        else:
            self.passport_department_info(message)

    def passport_department_info(self, message):
        """Показывает информацию о выбранном паспортном столе или возвращает к выбору."""
        response, website_url = self.get_department_info(message.text)
        if response:
            self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
            if website_url:
                self.bot.send_message(message.chat.id, f'Для получения актуальной информации перейдите на официальный сайт: [ссылка]({website_url})', parse_mode="Markdown")
        else:
            self.handle_unknown(message, self.show_passport_office_choice)

    def get_department_info(self, district_name):
        """Возвращает информацию о паспортном столе в зависимости от района."""
        info = {
            'Центрального района Гомеля': ("Информация о Центральном районе...", "https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1"),
            'Советского района Гомеля': ("Информация о Советском районе...", "https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1"),
            'Новобелицкого района Гомеля': ("Информация о Новобелицком районе...", "https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1"),
            'Железнодорожного района Гомеля': ("Информация о Железнодорожном районе...", "https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1"),
        }
        return info.get(district_name, (None, None))

    def show_final_choice(self, message):
        """Предлагает пользователю дальнейшие действия после предоставления информации."""
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton('Спасибо за информацию'), types.KeyboardButton('Вернуться назад'))
        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_final_choice)

    def handle_final_choice(self, message):
        """Обрабатывает выбор пользователя после предоставления информации о паспортном столе."""
        if message.text == 'Вернуться назад':
            self.show_passport_office_choice(message)
        elif message.text == 'Спасибо за информацию':
            self.bot.send_message(message.chat.id, "Рады были помочь! Если у вас есть ещё вопросы, вы всегда можете вернуться в главное меню.")
        else:
            self.handle_unknown(message, self.show_final_choice)