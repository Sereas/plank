from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

#BOT_TOKEN = str("2014222904:AAHNsExPuBAjWJ6SsX2otjwOp6WVz91u_Gg")
#ADMINS = str("327154479")  # Тут у нас будет список из админов
BOT_TOKEN = env.str("BOT_TOKEN") # Забираем значение типа str BOT_TOKEN
ADMINS = env.str("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

