import random

END = "\033[0m"
color_list = ["\033[0;31m", "\033[0;32m", "\033[0;33m",
              "\033[0;34m", "\033[0;35m", "\033[0;36m", "\033[0;37m"]


def custom(message: str, color: str): print(color + message + END)
def black(message: str): custom(message, "\033[0;30m")
def red(message: str): custom(message, "\033[0;31m")
def green(message: str): custom(message, "\033[0;32m")
def yellow(message: str): custom(message, "\033[0;33m")
def blue(message: str): custom(message, "\033[0;34m")
def purple(message: str): custom(message, "\033[0;35m")
def cyan(message: str): custom(message, "\033[0;36m")
def white(message: str): custom(message, "\033[0;37m")
def custom_word(message: str, word: str, color: str): print(message.replace(word, color + word + END))
def black_word(message: str, word: str): custom_word(message, word, "\033[0;30m")
def red_word(message: str, word: str): custom_word(message, word, "\033[0;31m")
def green_word(message: str, word: str): custom_word(message, word, "\033[0;32m")
def yellow_word(message: str, word: str): custom_word(message, word, "\033[0;33m")
def blue_word(message: str, word: str): custom_word(message, word, "\033[0;34m")
def purple_word(message: str, word: str): custom_word(message, word, "\033[0;35m")
def cyan_word(message: str, word: str): custom_word(message, word, "\033[0;36m")
def white_word(message: str, word: str): custom_word(message, word, "\033[0;37m")
def rand(message: str): custom(message, random.choice(color_list))
def hr(length, message="="): return message * len(length) if type(length) == str else message * length
def auto_hr(message: str): return message + "\n" + hr(message)


class CountLog:
    count = 0

    def log(self, message):
        custom(message, color_list[self.count])
        self.count = (self.count+1) % len(color_list)
