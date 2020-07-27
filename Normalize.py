from pymorphy2 import MorphAnalyzer
from subprocess import check_call
from sys import executable


class Normalizer:
    def __init__(self):
        self.morph = MorphAnalyzer()

    def norm(self, word):
        return self.morph.parse(word)[0].normal_form

