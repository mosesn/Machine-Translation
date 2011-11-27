from collections import defaultdict
from pprint import pprint
from time import time

def get_count(german_and_english):
    english_to_german = defaultdict(set)
    for german, english in german_and_english:
        german_split = german.split()
        for english_word in english.split():
            populate_set(english_to_german, english_word, german_split)

    ret_dict = {}
    for english, german_set in english_to_german.items():
        ret_dict[english] = len(german_set)
    return ret_dict, english_to_german

def populate_set(lexicon, key, values):
    for value in values:
        lexicon[key].add(value)

def generate_german_and_english(german_file, english_file):
    german_lst = get_file_list(german_file)
    english_lst = get_file_list(english_file)
    return zip(german_lst, english_lst)

def get_file_list(filename):
    fp = open(filename)
    lst = [line for line in fp]
    fp.close()
    return lst

class translators_dict(dict):
    def __init__(self, count_dict):
        self.count = count_dict

    def __missing__(self, key):
        self[key] = 1.0 / self.count[key[1]]
        return self[key]

def em(em_params, german_and_english):
    count = defaultdict(int)
    for german, english in german_and_english:
        german_split = german.split()
        english_split = english.split()
        for english_word in english_split:
            for german_word in german_split:
                change = delta(em_params, english_word, german_word, english_split)
                count[(german_word, english_word)] += change
                count[english_word] += change

    for key in em_params.keys():
        em_params[key] = count[key] / count[key[1]]

def delta(em_params, english_word, german_word, english_split):
    all_words_sum = sum([em_params[(german_word, eng)] for eng in english_split])
    return em_params[(german_word, english_word)] / all_words_sum

def get_best_words(em_params, english_to_german, filename):
    ret_list = []
    for english_line in get_file_list(filename):
        english = english_line.strip()
        cur_max = -1
        cur_best = None
        top_ten = sorted([(german, em_params[(german, english)]) for german in english_to_german[english]], reverse=True, key=lambda tup: tup[1])[:10]
        ret_list.append((english, top_ten))

    return ret_list

def get_best_alignment(em_params, german_and_english, num):
    ret_list = []
    for i in range(num):
        german, english = german_and_english[i]
        english_split = english.split()
        cur_list = []
        for german_word in german.split():
            cur_best = None
            cur_max = 0
            best_num = 0
            cur_num = 0
            for english_word in english_split:
                cur_num += 1
                params = em_params[(german_word, english_word)]
                if params > cur_max:
                    cur_max = params
                    cur_best = english_word
                    best_num = cur_num
            cur_list.append((german_word, cur_best, best_num))
        ret_list.append(cur_list)
    return ret_list

start = time()

german_english_lex = generate_german_and_english("../input/corpus.de",
                                    "../input/corpus.en")
ret_dict, english_german_sets = get_count(german_english_lex)
param_dict = translators_dict(ret_dict)

em(param_dict, german_english_lex)
em(param_dict, german_english_lex)
em(param_dict, german_english_lex)
em(param_dict, german_english_lex)
em(param_dict, german_english_lex)

print(time() - start)

pprint(get_best_words(param_dict, english_german_sets, "../input/devwords.txt"))

pprint(get_best_alignment(param_dict, german_english_lex, 20))

print(time() - start)
