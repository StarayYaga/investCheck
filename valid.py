from config import ownerId

class Valid():
    def __init__(self, bot):
        self.bot = bot

    def official(self, func):
        def wraper(message):
            id_tg = message.from_user.id
            if id_tg==ownerId:
                return func(message)
        return wraper