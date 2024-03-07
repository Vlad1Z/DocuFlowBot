from telebot import types
from .BaseHandler import BaseHandler
from utils import send_notification  # Убедитесь, что это правильный путь импорта


class CertificateHandler(BaseHandler):
    def handle(self, message):
        """Обрабатывает входящее сообщение и отображает опции справок."""
        self.show_certificate_options(message)

    def show_certificate_options(self, message):
        """Отображает пользователю клавиатуру с опциями различных справок, по одной опции на строку."""
        certificate_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Справка о месте жительства и составе семьи',
            'Справка о месте жительства',
            'Справка о занимаемом жилом помещении и составе семьи',
            'Справка о последнем месте жительства наследодателя и о составе его семьи',
            'Вернуться назад'
        ]
        for button in buttons:
            certificate_markup.row(types.KeyboardButton(button))
        # Отправляем сообщение с созданной клавиатурой пользователю
        self.bot.send_message(message.chat.id, "Выберите тип справки:", reply_markup=certificate_markup)
        # Регистрируем следующий обработчик для выбора пользователя
        self.bot.register_next_step_handler(message, self.process_certificate_choice)

    def process_certificate_choice(self, message):
        """Обрабатывает выбор пользователя после отображения клавиатуры справок."""
        choice_map = {
            'Справка о месте жительства и составе семьи': self.ask_for_address,
            'Справка о месте жительства': self.ask_for_address,
            'Справка о занимаемом жилом помещении и составе семьи': self.ask_for_address,
            'Справка о последнем месте жительства наследодателя и о составе его семьи': self.ask_for_address,
            'Вернуться назад': self.handle_back
        }
        # Получаем функцию обработчика для дальнейших действий или вызываем функцию для неизвестного выбора
        handler_function = choice_map.get(message.text, self.handle_unknown)
        handler_function(message)

    def ask_for_address(self, message):
        """Запрашивает у пользователя адрес проживания."""
        user_id = message.from_user.id
        # Проверяем, инициализирован ли словарь данных пользователя и инициализируем его при необходимости
        if not hasattr(self, 'user_data'):
            self.user_data = {}
        self.user_data[user_id] = {}
        self.bot.send_message(message.chat.id, "Введите адрес проживания (город, улица, дом):")
        self.bot.register_next_step_handler(message, self.ask_for_full_name)

    def ask_for_full_name(self, message):
        """Запрашивает у пользователя ФИО."""
        user_id = message.from_user.id
        self.user_data[user_id]['address'] = message.text
        self.bot.send_message(message.chat.id, "Введите ФИО полностью:")
        self.bot.register_next_step_handler(message, self.ask_for_birth_date)

    def ask_for_birth_date(self, message):
        """Запрашивает у пользователя дату рождения."""
        user_id = message.from_user.id
        # Используйте get для инициализации словаря, если он еще не создан для этого пользователя
        user_data = self.user_data.get(user_id, {})
        user_data['full_name'] = message.text  # Здесь предполагается, что message.text - это ФИО
        self.user_data[user_id] = user_data
        self.bot.send_message(message.chat.id, "Введите дату рождения (в формате ДД.ММ.ГГГГ):")
        self.bot.register_next_step_handler(message, self.ask_for_extra_details)

    def ask_for_extra_details(self, message):
        user_id = message.from_user.id
        address = self.user_data.get(user_id, {}).get('address', 'Не указано')
        full_name = self.user_data.get(user_id, {}).get('full_name', 'Не указано')
        birth_date = self.user_data.get(user_id, {}).get('birth_date', 'Не указано')
        extra_details = self.user_data.get(user_id, {}).get('extra_details', 'Не указано')
        confirmation_message = (
            "Пожалуйста, проверьте введенные данные:\n\n"
            f"Адрес: {address}\n"
            f"ФИО: {full_name}\n"
            f"Дата рождения: {birth_date}\n"
            f"Дополнительные сведения: {extra_details}"
        )
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Данные верны'))
        markup.add(types.KeyboardButton('Редактировать'))
        self.bot.send_message(message.chat.id, confirmation_message, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.final_confirmation)

    def final_confirmation(self, message):
        """Обрабатывает ответ пользователя на подтверждение данных."""
        user_id = message.from_user.id
        if message.text == 'Данные верны':
            # Данные подтверждены, можно их сохранять/обрабатывать
            self.complete_certificate_request(user_id)
        elif message.text == 'Редактировать':
            # Пользователь выбрал редактирование данных
            self.edit_user_data(user_id)
        else:
            # Пользователь отправил непредвиденный ответ, предлагаем ввести данные еще раз
            self.bot.send_message(message.chat.id, "Пожалуйста, выберите 'Данные верны' или 'Редактировать'.")
            self.ask_for_extra_details(message)

    def edit_user_data(self, message):
        """Позволяет пользователю редактировать введенные ранее данные."""
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Изменить адрес',
            'Изменить ФИО',
            'Изменить дату рождения',
            'Изменить дополнительные сведения',
            'Отмена'
        ]
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(user_id, "Какие данные вы хотите изменить?", reply_markup=markup)
        self.bot.register_next_step_handler_by_chat_id(user_id, self.process_edit_choice)

    def process_edit_choice(self, message):
        """Обрабатывает выбор пользователя при редактировании данных."""
        user_id = message.from_user.id
        # Проверяем, какие данные пользователь хочет изменить и вызываем соответствующий метод
        if message.text == 'Изменить адрес':
            self.ask_for_address(message)
        elif message.text == 'Изменить ФИО':
            self.ask_for_full_name(message)
        elif message.text == 'Изменить дату рождения':
            self.ask_for_birth_date(message)
        elif message.text == 'Изменить дополнительные сведения':
            self.ask_for_extra_details(message)
        elif message.text == 'Отмена':
            self.show_certificate_options(message)  # Отмена и возвращение к выбору справок
        else:
            self.bot.send_message(user_id, "Неизвестный выбор. Пожалуйста, попробуйте еще раз.")
            self.edit_user_data(user_id)

    def confirmation_and_save(self, message):
        """Сохраняет все данные справки и подтверждает пользователю завершение процесса."""
        user_id = message.from_user.id
        # Здесь можно реализовать логику проверки и сохранения данных, отправки их на сервер или в базу данных
        self.complete_certificate_request(user_id)

    def complete_certificate_request(self, user_id):
        """Завершает процесс заказа справки."""
        # Предполагаем, что данные пользователя уже сохранены в self.user_data[user_id]
        user_data = self.user_data.get(user_id, {})
        # Отправляем уведомление о новой заявке
        send_notification(user_id, user_data)
        # Уведомляем пользователя о принятии заявки
        self.bot.send_message(user_id, "Ваша заявка принята и будет обработана в ближайшее время.")

    def handle_back(self, message):
        """Возвращает пользователя в предыдущее меню."""
        from .StartHandler import StartHandler
        StartHandler(self.bot).handle(message)

    def handle_unknown(self, message):
        """Обрабатывает нераспознанный выбор пользователя и предлагает выбрать снова."""
        self.bot.send_message(message.chat.id, "Неизвестный выбор. Пожалуйста, попробуйте еще раз.")
        self.show_certificate_options(message)
