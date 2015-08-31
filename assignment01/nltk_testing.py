__author__ = 'tmkasun'

from nltk.book import text2

def frequency_dist(text, word):
    return text.count(word) * 100 / len(text)


def dispersion(text):
    return len(set(text)) * 100 / len(text)
