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
        response = ("📝 *Документы, необходимые для замены детского паспорта:*\n\n"
                    "👉 *Первичный паспорт:*\n"
                    "1️⃣ Четыре фотографии, подписанные с обратной стороны.\n"
                    "2️⃣ Оригинал свидетельства о рождении.\n"
                    "3️⃣ Паспорт одного из родителей.\n"
                    "4️⃣ Если ребенок старше 14 лет, необходимо оплатить госпошлину (оплата должна быть осуществлена по месту регистрации).\n\n"
                    "👉 *Продление паспорта:*\n"
                    "1️⃣ Четыре фотографии, подписанные с обратной стороны.\n"
                    "2️⃣ Копия свидетельства о рождении.\n"
                    "3️⃣ Если ребенок старше 14 лет, необходимо оплатить госпошлину (оплата должна быть осуществлена по месту регистрации).\n\n"
                    "🔍 *Дополнительная информация:*\n"
                    "🔸 Детям до 14 лет изготовление паспорта бесплатно.\n"
                    "🔸 При необходимости ускоренного изготовления документа также требуется предоставить квитанцию об уплате госпошлины за ускорение. Доступны варианты сроков изготовления: 7 и 15 дней.\n"
                    "🔸 Платно доступно SMS-оповещение о готовности паспорта.")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def show_adult_passport_info(self, message):
        # Показываем информацию о документах для взрослого паспорта
        response = ("📝 *Документы, необходимые для замены паспорта для взрослых:*\n\n"
                    "1️⃣ Четыре фотографии, подписанные с обратной стороны.\n"
                    "2️⃣ Копия свидетельства о рождении детей, если ребенок не достиг 16 лет.\n"
                    "3️⃣ Копия свидетельства о браке или решение суда о разводе.\n"
                    "   ❗️ *Важно:* В случаях смены фамилии из-за брака или развода, требуется оригинал документа для подтверждения текущей фамилии. Это относится к:\n"
                    "      - Возврату к девичьей фамилии после развода.\n"
                    "      - Смене фамилии после вступления в брак.\n"
                    "4️⃣ Квитанция об уплате госпошлины.\n\n"
                    "🔎 *Дополнительная информация:*\n"
                    "🔸 При необходимости ускоренного изготовления документа также требуется предоставить квитанцию об уплате госпошлины за ускорение. Доступны варианты сроков изготовления: 7 и 15 дней.\n"
                    "🔸 Платно доступно SMS-оповещение о готовности паспорта.")
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
