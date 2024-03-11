from telebot import types
from .BaseHandler import BaseHandler
from utils import send_notification
from datetime import datetime


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
        user_id = message.from_user.id
        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        # Здесь мы устанавливаем тип справки в user_data
        self.user_data[user_id]['certificate_type'] = message.text

        choice_map = {
            'Справка о месте жительства и составе семьи': self.ask_for_address,
            'Справка о месте жительства': self.ask_for_address,
            'Справка о занимаемом жилом помещении и составе семьи': self.ask_for_address,
            'Справка о последнем месте жительства наследодателя и о составе его семьи': self.ask_for_address,
            'Вернуться назад': self.handle_back
        }
        handler_function = choice_map.get(message.text)
        if handler_function:
            # Перед вызовом функции handler_function сохраняем тип справки
            handler_function(message)
        else:
            self.handle_unknown(message, self.show_certificate_options)

    def ask_for_address(self, message, return_to_confirmation=False):
        """Запрашивает у пользователя Адрес и сохраняет его."""
        self.bot.send_message(message.chat.id, "Введите адрес проживания (Город, улица, дом, корпус, квартира):")
        # Здесь определяем, какой обработчик будет вызван после валидации
        next_step_handler = self.save_address_and_confirm if return_to_confirmation else self.save_address
        # И уже здесь передаем message и next_step_handler в метод валидации
        self.bot.register_next_step_handler(message, lambda msg: self.validate_input(msg, next_step_handler))

    def save_address(self, message):
        user_id = message.from_user.id
        address = message.text.strip()
        if not BaseHandler.contains_two_numbers_and_text(address):
            msg = self.bot.send_message(message.chat.id,
                                        "Адрес введен некорректно. Убедитесь, что он содержит название улицы, номер дома, номер квартиры, и повторите попытку:")
            self.bot.register_next_step_handler(msg, self.save_address)
        else:
            self.user_data[user_id]['address'] = address
            self.ask_for_full_name(message)

    def save_address_and_confirm(self, message):
        user_id = message.from_user.id
        address = message.text.strip()
        if not BaseHandler.contains_two_numbers_and_text(address):
            msg = self.bot.send_message(message.chat.id,
                                        "Адрес введен некорректно. Убедитесь, что он содержит название улицы, номер дома, номер квартиры, и повторите попытку:")
            self.bot.register_next_step_handler(msg, self.save_address_and_confirm)
        else:
            self.user_data[user_id]['address'] = address
            self.confirm_and_display_data(message)

    def ask_for_full_name(self, message, return_to_confirmation=False):
        """Запрашивает у пользователя ФИО и сохраняет его."""
        self.bot.send_message(message.chat.id, "Введите ФИО полностью того, на кого оформляется справка:")
        next_step_handler = self.save_full_name_and_confirm if return_to_confirmation else self.save_full_name
        self.bot.register_next_step_handler(message, lambda msg: self.validate_input(msg, next_step_handler))

    def save_full_name(self, message):
        user_id = message.from_user.id
        full_name = message.text.strip()  # Удаляем лишние пробелы по краям
        # Простая проверка на количество слов в ФИО
        if len(full_name.split()) >= 3 and len(full_name) > 4:
            self.user_data[user_id]['full_name'] = full_name
            self.ask_for_birth_date(message)
        else:
            msg = self.bot.send_message(
                message.chat.id,
                "Пожалуйста, введите ваше полное ФИО."
            )
            self.bot.register_next_step_handler(msg, self.save_full_name)

    def save_full_name_and_confirm(self, message):
        user_id = message.from_user.id
        full_name = message.text.strip()  # Удаляем лишние пробелы по краям
        # Простая проверка на количество слов в ФИО
        if len(full_name.split()) >= 3 and len(full_name) > 4:
            self.user_data[user_id]['full_name'] = full_name
            self.confirm_and_display_data(message)
        else:
            msg = self.bot.send_message(
                message.chat.id,
                "Пожалуйста, введите ваше полное ФИО."
            )
            self.bot.register_next_step_handler(msg, self.save_full_name_and_confirm)

    def ask_for_birth_date(self, message, return_to_confirmation=False):
        user_id = message.from_user.id
        self.bot.send_message(message.chat.id, "Введите дату рождения (в формате ДД.ММ.ГГГГ):")
        if return_to_confirmation:
            next_step_handler = self.save_birth_date_and_confirm
        else:
            next_step_handler = self.save_birth_date
        self.bot.register_next_step_handler(message, next_step_handler)

    def save_birth_date(self, message):
        """Сохраняет дату рождения пользователя после проверки валидности."""
        user_id = message.from_user.id
        date_text = message.text
        try:
            # Попытка преобразовать текст в дату
            birth_date = datetime.strptime(date_text, '%d.%m.%Y')
            # Если дата корректна, сохраняем и переходим к следующему шагу
            self.user_data[user_id]['birth_date'] = birth_date.strftime('%d.%m.%Y')
            self.ask_for_number_of_certificates(message)
        except ValueError:
            # Если дата некорректна, просим ввести снова
            msg = self.bot.send_message(
                message.chat.id,
                "Дата введена некорректно. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:"
            )
            self.bot.register_next_step_handler(msg, self.save_birth_date)

    def save_birth_date_and_confirm(self, message):
        """Сохраняет Дату рождения пользователя и возвращает его к подтверждению данных."""
        user_id = message.from_user.id
        date_text = message.text
        try:
            # Попытка преобразовать текст в дату
            birth_date = datetime.strptime(date_text, '%d.%m.%Y')
            # Если дата корректна, сохраняем и продолжаем
            self.user_data[user_id]['birth_date'] = birth_date.strftime('%d.%m.%Y')
            self.confirm_and_display_data(message)
        except ValueError:
            # Если дата некорректна, просим ввести снова
            msg = self.bot.send_message(message.chat.id,
                                        "Дата введена некорректно. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:")
            self.bot.register_next_step_handler(msg, self.save_birth_date_and_confirm)

    def ask_for_number_of_certificates(self, message, return_to_confirmation=False):
        user_id = message.from_user.id
        self.bot.send_message(message.chat.id, "Введите необходимое количество справок:")
        if return_to_confirmation:
            next_step_handler = self.save_number_of_certificates_and_confirm
        else:
            next_step_handler = self.save_number_of_certificates
        self.bot.register_next_step_handler(message, next_step_handler)

    def save_number_of_certificates(self, message):
        user_id = message.from_user.id
        try:
            number = int(message.text)
            if not 1 <= number <= 10:
                raise ValueError
            self.user_data[user_id]['number_of_certificates'] = number
            self.ask_for_extra_details(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
            # Повторно запросите ввод количества справок, если ввод некорректен
            self.bot.register_next_step_handler(message, self.save_number_of_certificates)

    def save_number_of_certificates_and_confirm(self, message):
        """Сохраняет необходимое Количество справок пользователя и возвращает его к подтверждению данных."""
        user_id = message.from_user.id
        try:
            number = int(message.text)
            if not 1 <= number <= 10:
                raise ValueError
            self.user_data[user_id]['number_of_certificates'] = number
            self.confirm_and_display_data(message)
        except ValueError:
            self.bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")
            # Повторно запросите ввод количества справок, если ввод некорректен
            self.bot.register_next_step_handler(message, self.save_number_of_certificates)

    def ask_for_extra_details(self, message, return_to_confirmation=False):
        """Запрашивает у пользователя дополнительные сведения и сохраняет их."""
        self.bot.send_message(message.chat.id, "Введите дополнительные сведения (если необходимо):")
        next_step_handler = self.save_extra_details_and_confirm if return_to_confirmation else self.save_extra_details
        self.bot.register_next_step_handler(message,
                                            lambda msg: self.validate_input(msg, next_step_handler))

    def save_extra_details(self, message):
        user_id = message.from_user.id
        self.user_data[user_id]['extra_details'] = message.text
        self.confirm_and_display_data(message)

    def save_extra_details_and_confirm(self, message):
        """Сохраняет Дополнительные сведения пользователя и возвращает его к подтверждению данных."""
        user_id = message.from_user.id
        self.user_data[user_id]['extra_details'] = message.text
        self.confirm_and_display_data(message)

    def confirm_and_display_data(self, message):
        user_id = message.from_user.id
        # Здесь уже все данные сохранены, просто извлекаем их для подтверждения
        address = self.user_data[user_id].get('address', 'Не указан')
        full_name = self.user_data[user_id].get('full_name', 'Не указано')
        birth_date = self.user_data[user_id].get('birth_date', 'Не указана')
        number_of_certificates = self.user_data[user_id].get('number_of_certificates', 'Не указана')
        extra_details = self.user_data[user_id].get('extra_details', 'Не указано')
        certificate_type = self.user_data[user_id].get('certificate_type', 'Не указано')

        confirmation_message = f"""Пожалуйста, проверьте введенные данные:

    Тип справки: {certificate_type}
    Адрес: {address}
    ФИО: {full_name}
    Дата рождения: {birth_date}
    Количество справок: {number_of_certificates}
    Дополнительные сведения: {extra_details}"""

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Данные верны'), types.KeyboardButton('Редактировать'))
        self.bot.send_message(message.chat.id, confirmation_message, reply_markup=markup)
        self.bot.register_next_step_handler(message, self.final_confirmation)

    def final_confirmation(self, message):
        """Обрабатывает ответ пользователя на подтверждение данных."""
        user_info = message.from_user
        user_name = f"{user_info.first_name} {user_info.last_name}" if user_info.last_name else user_info.first_name
        user_id = user_info.id
        username = user_info.username
        # Телефонный номер нельзя получить напрямую через message.from_user, его можно получить только если пользователь явно отправил его через специальный интерфейс.
        # phone_number = user_info.phone_number if hasattr(user_info, 'phone_number') else 'Не указан'

        if message.text == 'Данные верны':
            # Данные подтверждены, можно их сохранять/обрабатывать
            user_data = self.user_data.get(user_id, {})
            # Подготовка строки с информацией о пользователе
            user_info_str = (
                f"Имя: {user_name}\n"
                f"ID: {user_id}\n"
                f"Username: @{username}")
            # Передаем эту строку в функцию отправки уведомления
            send_notification(user_id, user_data, user_info_str)
            # Здесь ваш код для обработки и сохранения данных заявки...
            # self.complete_certificate_request(user_id)
            self.show_final_choice(message)
        elif message.text == 'Редактировать':
            # Пользователь выбрал редактирование данных
            self.edit_user_data(message)  # Убедитесь, что edit_user_data правильно обрабатывает передачу message
        else:
            self.handle_unknown(message, self.confirm_and_display_data)

    def edit_user_data(self, message):
        """Позволяет пользователю редактировать введенные ранее данные."""
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = [
            'Изменить адрес',
            'Изменить ФИО',
            'Изменить дату рождения',
            'Изменить количество справок',
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
        if message.text == 'Изменить адрес':
            self.ask_for_address(message, return_to_confirmation=True)
        elif message.text == 'Изменить ФИО':
            self.ask_for_full_name(message, return_to_confirmation=True)
        elif message.text == 'Изменить дату рождения':
            self.ask_for_birth_date(message, return_to_confirmation=True)
        elif message.text == 'Изменить количество справок':
            self.ask_for_number_of_certificates(message, return_to_confirmation=True)
        elif message.text == 'Изменить дополнительные сведения':
            self.ask_for_extra_details(message, return_to_confirmation=True)
        elif message.text == 'Отмена':
            self.confirm_and_display_data(message)
        else:
            self.handle_unknown(message, self.confirm_and_display_data)

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

    def show_final_choice(self, message):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        buttons = ["Заказать еще справку", "Вернуться в главное меню", "Спасибо за информацию"]
        for button in buttons:
            markup.add(types.KeyboardButton(button))
        self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        self.bot.register_next_step_handler(message, self.handle_final_choice)

    def handle_final_choice(self, message):
        if message.text == "Заказать еще справку":
            self.show_certificate_options(message)
        elif message.text == "Вернуться в главное меню":
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        elif message.text == "Спасибо за информацию":
            self.bot.send_message(message.chat.id, "Спасибо! Если у вас возникнут дополнительные вопросы, вы всегда можете к нам обратиться.")
        else:
            self.bot.send_message(message.chat.id, "Неизвестная команда, пожалуйста, выберите один из предложенных вариантов.")
            self.show_final_choice(message)  # Предложить пользователю снова сделать выбор
