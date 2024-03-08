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
