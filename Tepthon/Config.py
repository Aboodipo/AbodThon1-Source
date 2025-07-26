import os

class Config:
    API_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "")
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", -100))
    PM_LOGGER_GROUP_ID = int(os.environ.get("PM_LOGGER_GROUP_ID", -100))
    ALIVE_NAME = os.environ.get("ALIVE_NAME", "Tepthon")
    ENV = os.environ.get("ENV", "ANYTHING")
    HEROKU_APP = None  # render ما يستخدم Heroku
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", ".")
