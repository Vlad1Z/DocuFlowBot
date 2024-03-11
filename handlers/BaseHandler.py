
import re


class BaseHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}

    def handle(self, message):
        raise NotImplementedError("Этот метод должен быть переопределен.")

    def handle_back(self, message):
        """Возвращает пользователя в предыдущее меню."""
        from .StartHandler import StartHandler  # Предполагается, что StartHandler - это ваш начальный обработчик
        StartHandler(self.bot).handle(message)

    def handle_unknown(self, message, repeat_menu_method=None):
        """Обрабатывает нераспознанный выбор пользователя и предлагает выбрать снова."""
        self.bot.send_message(message.chat.id, "Извините, я не понял ваш выбор. Пожалуйста, выберите один из предложенных вариантов.")
        if repeat_menu_method:
            repeat_menu_method(message)

    def contains_two_numbers_and_text(string):
        # Проверяем, содержит ли строка минимум два числа
        numbers_found = len(re.findall(r'\d+', string)) >= 2
        # Проверяем, содержит ли строка буквенные символы (предполагаем, что это может быть название улицы)
        contains_text = bool(re.search(r'[a-zA-Zа-яА-Я]', string))
        return numbers_found and contains_text

    import re

    def validate_input(self, message, next_step_handler, validation_rules=None):
        """
        Общий метод для валидации ввода пользователя.
        :param message: Сообщение от пользователя.
        :param next_step_handler: Функция-обработчик для следующего шага.
        :param validation_rules: Словарь с правилами валидации (например, максимальная длина, запрет ссылок).
        """
        user_id = message.from_user.id
        text = message.text.strip()
        error_messages = []

        if validation_rules is None:
            validation_rules = {}

        # Проверяем максимальную длину
        max_length = validation_rules.get("max_length", 100)
        if len(text) > max_length:
            error_messages.append(f"Текст не должен превышать {max_length} символов.")

        # Проверяем наличие ссылок
        if validation_rules.get("no_links", False):
            if re.search(r"https?://", text):
                error_messages.append("Пожалуйста, не отправляйте ссылки.")

        # Если есть ошибки валидации, отправляем сообщение с ошибкой и просим ввести снова
        if error_messages:
            error_text = "\n".join(error_messages) + "\nПожалуйста, попробуйте ввести снова:"
            msg = self.bot.send_message(message.chat.id, error_text)
            self.bot.register_next_step_handler(msg,
                                                lambda m: self.validate_input(m, next_step_handler, validation_rules))
        else:
            # Если все в порядке, вызываем следующий обработчик
            next_step_handler(message)

