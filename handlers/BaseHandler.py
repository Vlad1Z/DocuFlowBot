class BaseHandler:
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}

    def handle(self, message):
        raise NotImplementedError("Этот метод должен быть переопределен.")
