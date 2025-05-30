from telebot import types


class StartHandler:
    """
    Класс StartHandler управляет начальным взаимодействием с пользователем,
    включая отображение главного меню и приветственного сообщения.
    """
    def __init__(self, bot):
        """Инициализирует обработчик с экземпляром бота. :param bot: Экземпляр телеграм-бота."""
        self.bot = bot

    def handle(self, message, is_welcome=False):
        """
        Вызывает отображение главного меню, опционально с приветственным сообщением.
        :param message: Сообщение от пользователя.
        :param is_welcome: Булевый параметр, определяющий, следует ли отображать приветственное сообщение.
        """
        # self.bot.delete_state(message.from_user.id)
        self.main_menu(message, is_welcome)

    def send_help_message(self, message):
        """Отправляет сообщение с помощью пользователю."""
        help_text = (
            "Здесь вы можете узнать, как пользоваться ботом:\n"
            "/start - начать работу с ботом\n"
            "/help - получить справку по командам\n"
            "… и так далее для каждой команды."
        )
        self.bot.send_message(message.chat.id, help_text)

    def main_menu(self, message, is_welcome=False):
        """
        Отображает главное меню бота с помощью клавиатуры. При is_welcome=True отправляется
        приветственное сообщение с описанием возможностей бота.

        :param message: Сообщение от пользователя.
        :param is_welcome: Если True, отображается приветственное сообщение.
        """
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Заказать справку',
                   'Узнать перечень документов на замену паспорта',
                   'Узнать перечень документов для регистрации (прописки)',
                   'Получить информацию о работе паспортных столов г. Гомель']
        for button in buttons:
            markup.add(types.KeyboardButton(button))

        if is_welcome:
            welcome_text = (
                "👋 Привет! Я помощник для получения различных справок и информации о документах.\n\n"
                "Вот что я могу делать:\n"
                "- 🏛 Получить информацию о паспортных столах.\n"
                "- 📄 Узнать, какие документы нужны для оформления паспорта.\n"
                "- 📑 Заказать справки.\n"
                "- 🏠 Получить информацию о документах для регистрации в жилое помещение.\n\n"
                "Чтобы начать, просто выберите интересующую вас опцию из меню или введите команду.\n\n"
                # "Если вам нужна помощь, введите /help."
            )
        else:
            welcome_text = "Выберите опцию из меню ниже:"

        self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)







