from .BaseHandler import BaseHandler
from telebot import types


class RegistrationInfoHandler(BaseHandler):
    def handle(self, message):
        """Обрабатывает начальное сообщение пользователя и отображает меню с выбором типа регистрации."""
        self.show_registration_type_choice(message)

    def show_registration_type_choice(self, message):

        registration_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        registration_markup.add(
            types.KeyboardButton('Собственник квартиры'),
            types.KeyboardButton('Дети собственника (несовершеннолетние)'),
            types.KeyboardButton('Дети собственника (достижение 18 лет)'),
            types.KeyboardButton('Супруг(а) собственника'),
            types.KeyboardButton('Лица, не являющиеся родственниками'),
            types.KeyboardButton('Вернуться назад')
        )
        self.bot.send_message(message.chat.id, "Выберите тип регистрации:", reply_markup=registration_markup)
        self.bot.register_next_step_handler(message, self.registration_type)

    def registration_type(self, message):
        """Показывает информацию о выбранном паспортном столе или возвращает к выбору."""
        if message.text == 'Собственник квартиры':
            self.send_owner_docs_info(message)
        elif message.text == 'Дети собственника (несовершеннолетние)':
            self.send_owner_children_docs_info(message)
        elif message.text == 'Дети собственника (достижение 18 лет)':
            self.send_adult_children_docs_info(message)
        elif message.text == 'Супруг(а) собственника':
            self.send_spouse_docs_info(message)
        elif message.text == 'Лица, не являющиеся родственниками':
            self.send_non_relative_docs_info(message)
        elif message.text == 'Вернуться назад':
            from .StartHandler import StartHandler
            StartHandler(self.bot).handle(message)
        else:
            self.handle_unknown(message, self.show_registration_type_choice)

    def send_owner_docs_info(self, message):
        """Отправляет информацию о документах для регистрации собственника квартиры."""
        response = (
            "📝 *Документы для собственника квартиры:*\n\n"
            "1️⃣ Наличие собственника квартиры.\n"
            "2️⃣ Паспорт собственника.\n"
            "3️⃣ Регистрационное свидетельство на квартиру из БТИ (оригинал).\n"
            "4️⃣ Квитанция об уплате госпошлины.\n"
            "5️⃣ Военный билет с отметкой о постановке на воинский учет по новому адресу (для военнообязанных).\n\n"
            "💳 *Пути оплаты госпошлины за регистрационный документ:*\n"
            "🔹 Ерип - МВД - Гражданство и миграция - для граждан Белоруси - г. Гомель - Выбрать район - Регист-я жительства/пребывания.\n\n")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def send_owner_children_docs_info(self, message):
        """Отправляет информацию о документах для регистрации несовершеннолетних детей собственника."""
        response = (
            "📝 *Документы для регистрации несовершеннолетних детей собственника:*\n\n"
            "1️⃣ Паспорт одного из родителей.\n"
            "2️⃣ Паспорт и свидетельство о рождении ребенка (оригинал).\n"
            "    ❗️ *Важно:* Если один из родителей зарегистрирован по другому адресу, "
            "необходимо согласие на регистрацию ребенка.\n"
            "3️⃣Согласие можно получить у паспортиста или в РСЦ.")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def send_adult_children_docs_info(self, message):
        """Отправляет информацию о документах для регистрации совершеннолетних детей собственника."""
        response = (
            "📝 *Документы для регистрации совершеннолетних детей собственника:*\n\n"
            "1️⃣ Паспорт.\n"
            "2️⃣ Свидетельство о рождении (оригинал).\n"
            "3️⃣ Квитанция об уплате госпошлины.\n"
            "4️⃣ Военный билет с отметкой о постановке на воинский учет по новому адресу (для военнообязанных).\n\n"
            "💳 *Пути оплаты госпошлины за регистрационный документ:*\n"
            "🔹 Ерип - МВД - Гражданство и миграция - для граждан Белоруси - г. Гомель - Выбрать район - Регист-я жительства/пребывания.\n\n")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def send_spouse_docs_info(self, message):
        """Отправляет информацию о документах для регистрации супруга(и) собственника."""
        response = (
            "📝 *Документы для регистрации супруга(и) собственника:*\n\n"
            "1️⃣ Наличие собственника квартиры.\n"
            "2️⃣ Паспорт.\n"
            "3️⃣ Свидетельство о браке (оригинал).\n"
            "4️⃣ Квитанция об уплате госпошлины.\n"
            "5️⃣ Военный билет с отметкой о постановке на воинский учет по новому адресу (для военнообязанных).\n\n"
            "💳 *Пути оплаты госпошлины за регистрационный документ:*\n"
            "🔹 Ерип - МВД - Гражданство и миграция - для граждан Белоруси - г. Гомель - Выбрать район - Регист-я жительства/пребывания.\n\n")
        self.bot.send_message(message.chat.id, response, parse_mode="Markdown")
        self.show_final_choice(message)

    def send_non_relative_docs_info(self, message):
        """Отправляет информацию о документах для регистрации лиц, не являющихся родственниками."""
        response = (
            "📝 *Документы для регистрации лиц, не являющихся родственниками:*\n\n"
            "1️⃣ Паспорт.\n"
            "2️⃣ Договор найма жилого помещения (оригинал).\n"
            "   ❗️ *Важно:* Договор заключается в администрации района.\n"
            "️4️⃣ Квитанция об уплате госпошлины.\n\n"
            "💳 *Пути оплаты госпошлины за регистрационный документ:*\n"
            "🔹 Ерип - МВД - Гражданство и миграция - для граждан Белоруси - г. Гомель - Выбрать район - Регист-я жительства/пребывания.\n\n")
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
            self.show_registration_type_choice(message)
        elif message.text == 'Спасибо за информацию':
            self.bot.send_message(message.chat.id, "Рады были помочь! Если у вас есть ещё вопросы, вы всегда можете вернуться в главное меню.")
        else:
            self.handle_unknown(message, self.show_final_choice)