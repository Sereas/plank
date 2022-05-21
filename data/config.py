from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN") # Забираем значение типа str BOT_TOKEN
ADMINS = list(map(int, env.list("ADMINS")))  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
USER = env.str("USER")
PASSWORD = env.str("PASSWORD")
HOST = env.str("HOST")
PORT = env.str("PORT")
DATABASE = env.str("DATABASE")
