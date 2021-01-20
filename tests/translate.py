import sys
from googletrans import Translator

def translate(text):
    translator = Translator()
    result = translator.translate(text, dest='zh-cn', src='en',)
    return result.text

if __name__ == '__main__':
    text = sys.argv[1]
    print(translate(text))
