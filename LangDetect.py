# -*- coding: utf8 -*-
from recobj.data.languages import *


def split_by_words(str):
    split_words = []
    signs = set([',', '.', '?', '!', '"', '(', ')', ':', '-'])
    for w in str.split(' '):
        while len(w) > 0 and w[len(w) - 1] in signs:
            w = w[:len(w) - 1]
        if len(w) > 0:
            split_words.append(w.lower())
    return split_words


def get_ru_word(str, dict):
    for i in dict:
        str = str.replace(i, dict[i])
    return str


def detect_language(text, accuracy=0.2, base_dict=None, spechal_dict=None):
    if base_dict is None:
        base_dict = base_dictionary
    if spechal_dict is None:
        spechal_dict = spechal_dictionary
    words = split_by_words(text)
    lang = 'un'
    lang_count = 0
    for cur_lang in base_dict:
        cur_lang_count = 0
        for w in words:
            if w in cur_lang[0]:
                cur_lang_count += 1
        if cur_lang_count > lang_count and cur_lang_count / len(words) >= accuracy:
            lang = cur_lang[1]
            lang_count = cur_lang_count
    if lang == 'un':
        for cur_lang in spechal_dict:
            cur_lang_count = 0
            for ch in text:
                if ch in cur_lang[0]:
                    cur_lang_count += 1
                if cur_lang_count > lang_count and cur_lang_count / len(text) >= accuracy:
                    lang = cur_lang[1]
                    lang_count = cur_lang_count
    return lang


def translit_into_ru(text, accuracy=0.1, translit_dicts=None):
    if translit_dicts is None:
        translit_dicts = default_translit_dictionaries
    words = split_by_words(text)
    best_transl_words_detected = 0
    best_transl_ind = -1
    ru_dict = set(ru)
    for i, transl in enumerate(translit_dicts):
        cur_transl_words_detected = 0
        for w in words:
            if get_ru_word(w, transl) in ru_dict:
                cur_transl_words_detected += 1
        if cur_transl_words_detected >= best_transl_words_detected:
            best_transl_words_detected = cur_transl_words_detected
            best_transl_ind = i
    if best_transl_ind != -1 and best_transl_words_detected / len(words) >= accuracy:
        for i in translit_dicts[best_transl_ind]:
            text = text.replace(i, translit_dicts[best_transl_ind][i])
        return text
    return None
