from .BaseHandler import BaseHandler
from telebot import types


class PassportOfficeInfoHandler(BaseHandler):
    def handle(self, message):
        """Обработка начального сообщения и показ выбора паспортного стола."""
        self.show_passport_office_choice(message)

    def show_passport_office_choice(self, message):
        """Показывает пользователю кнопки для выбора районного паспортного стола."""
        department_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        department_markup.add(
            types.KeyboardButton('Центрального района Гомеля'),
            types.KeyboardButton('Советского района Гомеля'),
            types.KeyboardButton('Новобелицкого района Гомеля'),
            types.KeyboardButton('Железнодорожного района Гомеля'),
            types.KeyboardButton('Вернуться назад')
        )
        self.bot.send_message(message.chat.id, "Выберите паспортный стол:", reply_markup=department_markup)
        self.bot.register_next_step_handler(message, self.department_type)

    def department_type(self, message):
        """Показывает информацию о выбранном паспортном столе или возвращает к выбору."""
        if message.text == 'Центрального района Гомеля':
            self.central_district_info(message)
        elif message.text == 'Советского района Гомеля':
            self.soviet_district_info(message)
        elif message.text == 'Новобелицкого района Гомеля':
            self.novobelitsa_district_info(message)
        elif message.text == 'Железнодорожного района Гомеля':
            self.railway_district_info(message)
        elif message.text == 'Вернуться назад':
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        else:
            self.handle_unknown(message, self.show_passport_office_choice)

    def central_district_info(self, message):
        info = (
            "🏛 *Паспортный стол Центрального района Гомеля*\n\n"
            "📍 Адрес: ул. Крестьянская, д.42\n"
            "⏰ Время работы:\n    Вт, Пт: 8:00–17:00\n    Ср: 11:00-20:00\n    Чт, Сб: 08:00-13:00\n"
            "📞 Телефоны:\n    +375(232)742-155\n    +375(232)701-530\n    +375(232)751-896\n"
            "📬 Индекс: 246002\n\n"
            "🔗 Информация может изменяться, с актуальными данными можно ознакомиться на [официальном сайте](https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1)"
        )
        self.bot.send_message(message.chat.id, info, parse_mode="Markdown", disable_web_page_preview=True)
        self.show_final_choice(message)

    def soviet_district_info(self, message):
        info = (
            "🏛 *Паспортный стол Советского района Гомеля*\n\n"
            "📍 Адрес: Речицкий проспект, д. 55\n"
            "⏰ Время работы:\n    Вт, Пт: 8:00–17:00\n    Ср: 11:00-20:00\n    Чт, Сб: 08:00-13:00\n"
            "📞 Телефоны:\n    +375(232)434-398\n    +375(232)434-942\n    +375(232)434-211\n    +375(232)435-935\n"
            "📬 Индекс: 246012\n\n"
            "🔗 Информация может изменяться, с актуальными данными можно ознакомиться на [официальном сайте](https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1)"
        )
        self.bot.send_message(message.chat.id, info, parse_mode="Markdown", disable_web_page_preview=True)
        self.show_final_choice(message)

    def novobelitsa_district_info(self, message):
        info = (
            "🏛 *Паспортный стол Новобелицкого района Гомеля*\n\n"
            "📍 Адрес: ул.Степана Разина, д.9\n"
            "⏰ Время работы:\n    Вт, Пт: 8:00–17:00\n    Ср: 11:00-20:00\n    Чт, Сб: 08:00-13:00\n"
            "📞 Телефоны:\n    +375(232)362 658\n"
            "📬 Индекс: 246042\n\n"
            "🔗 Информация может изменяться, с актуальными данными можно ознакомиться на [официальном сайте](https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1)"
        )
        self.bot.send_message(message.chat.id, info, parse_mode="Markdown", disable_web_page_preview=True)
        self.show_final_choice(message)

    def railway_district_info(self, message):
        info = (
            "🏛 *Паспортный стол Железнодорожного района Гомеля*\n\n"
            "📍 Адрес: ул.Кирова, д.122\n"
            "⏰ Время работы:\n    Вт, Пт: 8:00–17:00\n    Ср: 11:00-20:00\n    Чт, Сб: 08:00-13:00\n"
            "📞 Телефон: +375(232)609-486\n"
            "📬 Индекс: 246028\n\n"
            "🔗 Информация может изменяться, с актуальными данными можно ознакомиться на [официальном сайте](https://creditportal.by/info/pasportnyj-stol-v-gomele.html#i1)"
        )
        self.bot.send_message(message.chat.id, info, parse_mode="Markdown", disable_web_page_preview=True)
        self.show_final_choice(message)

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