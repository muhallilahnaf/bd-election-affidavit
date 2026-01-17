from pathlib import Path
from os.path import join
import json
from tqdm import tqdm
from rapidfuzz import fuzz
import re


# folder paths
directory = Path("data/text/ereturn")
dir_cert = Path("data/text/ereturn/certificate")
dir_slip = Path("data/text/ereturn/slip")

# list of certificate and slip text files
certificate_files = [p.name for p in dir_cert.iterdir()]
slip_files = [p.name for p in dir_slip.iterdir()]

# store data
store = {}

def get_cert_name(words, phrase_list, i, window_size):
    name = ''
    phrase_name = 'taxpayers name'
    phrase_name_len = len(phrase_name.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_name_len, window_size)])
    ending_word = 'taxpayers'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_name) > 85:
        start = i + phrase_name_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            name = ' '.join(words[start:j])
    return name

def get_cert_tin(words, phrase_list, i, window_size):
    tin = ''
    phrase_tin = 'taxpayers identification number'
    phrase_tin_len = len(phrase_tin.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_tin_len, window_size)])
    ending_word = 'fathers'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_tin) > 85:
        start = i + phrase_tin_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            tin = ' '.join(words[start:j])
        tin = re.sub(r'\D+', '', tin)
    return tin

def get_cert_father(words, phrase_list, i, window_size):
    father = ''
    phrase_father = 'fathers name'
    phrase_father_len = len(phrase_father.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_father_len, window_size)])
    ending_word = 'mothers'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_father) > 85:
        start = i + phrase_father_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            father = ' '.join(words[start:j])
    return father

def get_cert_mother(words, phrase_list, i, window_size):
    mother = ''
    phrase_mother = 'mothers name'
    phrase_mother_len = len(phrase_mother.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_mother_len, window_size)])
    ending_word = 'current'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_mother) > 85:
        start = i + phrase_mother_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            mother = ' '.join(words[start:j])
    return mother

def get_cert_current_addr(words, phrase_list, i, window_size):
    current_addr = ''
    phrase_current_addr = 'current address'
    phrase_current_addr_len = len(phrase_current_addr.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_current_addr_len, window_size)])
    ending_word = 'permanent'
    lookahead_size = 30
    if fuzz.ratio(phrase, phrase_current_addr) > 85:
        start = i + phrase_current_addr_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            current_addr = ' '.join(words[start:j])
    return current_addr

def get_cert_permanent_addr(words, phrase_list, i, window_size):
    permanent_addr = ''
    phrase_permanent_addr = 'permanent address'
    phrase_permanent_addr_len = len(phrase_permanent_addr.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_permanent_addr_len, window_size)])
    ending_word = 'status'
    lookahead_size = 30
    if fuzz.ratio(phrase, phrase_permanent_addr) > 85:
        start = i + phrase_permanent_addr_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            permanent_addr = ' '.join(words[start:j])
    return permanent_addr

def get_cert_shown(words, phrase_list, i, window_size):
    shown = ''
    phrase_shown = 'shown total income'
    phrase_shown_len = len(phrase_shown.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_shown_len, window_size)])
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_shown) > 85:
        start = i + phrase_shown_len
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        shown = ' '.join(words[start:end])
        shown = re.sub(r'\D+', '', shown)
    return shown

def get_cert_wealth(words, phrase_list, i, window_size):
    wealth = ''
    phrase_wealth = 'net wealth'
    phrase_wealth_len = len(phrase_wealth.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_wealth_len, window_size)])
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_wealth) > 85:
        start = i + phrase_wealth_len
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        wealth = ' '.join(words[start:end])
        wealth = re.sub(r'\D+', '', wealth)
    return wealth

def get_cert_paid(words, phrase_list, i, window_size):
    paid = ''
    phrase_paid = 'paid tax'
    phrase_paid_len = len(phrase_paid.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_paid_len, window_size)])
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_paid) > 85:
        start = i + phrase_paid_len
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        paid = ' '.join(words[start:end])
        paid = re.sub(r'\D+', '', paid)
    return paid

def get_slip_name(words, phrase_list, i, window_size):
    name = ''
    phrase_name = 'name of the taxpayer'
    phrase_name_len = len(phrase_name.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_name_len, window_size)])
    ending_word = 'nid'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_name) > 85:
        start = i + phrase_name_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            name = ' '.join(words[start:j])
    return name

def get_slip_nid(words, phrase_list, i, window_size):
    nid = ''
    phrase_nid = 'passport no if no nid'
    phrase_nid_len = len(phrase_nid.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_nid_len, window_size)])
    ending_word = 'circle'
    lookahead_size = 8
    if fuzz.ratio(phrase, phrase_nid) > 85:
        start = i + phrase_nid_len
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            nid = ' '.join(words[start:j])
            nid = re.sub(r'\D+', '', nid)
    return nid

def get_slip_shown(words, phrase_list, i, window_size):
    shown = ''
    phrase_shown = 'total income shown'
    phrase_shown_len = len(phrase_shown.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_shown_len, window_size)])
    lookahead_size = 5
    if fuzz.ratio(phrase, phrase_shown) > 85:
        start = i + phrase_shown_len
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        shown = ' '.join(words[start:end])
        shown = re.sub(r'\D+', '', shown)
    return shown

def get_slip_paid(words, phrase_list, i, window_size):
    paid = ''
    phrase_paid = 'total tax paid'
    phrase_paid_len = len(phrase_paid.split(' '))
    phrase = ' '.join(phrase_list[:min(phrase_paid_len, window_size)])
    lookahead_size = 5
    if fuzz.ratio(phrase, phrase_paid) > 85:
        start = i + phrase_paid_len
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        paid = ' '.join(words[start:end])
        paid = re.sub(r'\D+', '', paid)
    return paid


# for full text
def get_text_data(words, phrase_list, item_phrase_list, i):
    value = ''
    item_phrase_len = len(item_phrase_list)
    item_phrase = ' '.join(item_phrase_list)
    phrase = ' '.join(phrase_list)
    lookahead_size = 10
    if fuzz.token_set_ratio(phrase, item_phrase) > 85:
        value_words = words[i: min(i+item_phrase_len+lookahead_size, len(words))]
        for word in value_words:
            if word not in item_phrase_list:
                value = value + word + ' '
    return value.strip()


# filter out empty string and only special chars from word list
def filter_words(words):
    filtered = []
    for word in words:
        word = word.strip()
        if word == '':
            continue
        word = re.sub(r'\W+', '', word)
        if word == '':
            continue
        filtered.append(word)
    return filtered


# main loop
# loop through text files
for p in tqdm(list(directory.iterdir())):
    if p.is_file():
        try:
            store[p.name] = {}
            # extract from certificate page
            if p.name in certificate_files:
                with open(join(dir_cert.absolute(), p.name), 'r') as f:
                    text = f.read().replace('\n', ' ').lower()
                    words_raw = text.split(' ')
                    words = filter_words(words_raw)
                    window_size = 3

                    name = ''
                    tin = ''
                    father = ''
                    mother = ''
                    current_addr = ''
                    permanent_addr = ''
                    shown = ''
                    wealth = ''
                    paid = ''   

                    for i, word in enumerate(words):
                        # sliding window
                        phrase_list = words[i:min(i+window_size, len(words))]
                        
                        if name == '':
                            name = get_cert_name(words, phrase_list, i, window_size)
                        if tin == '':
                            tin = get_cert_tin(words, phrase_list, i, window_size)
                        if father == '':
                            father = get_cert_father(words, phrase_list, i, window_size)
                        if mother == '':
                            mother = get_cert_mother(words, phrase_list, i, window_size)
                        if current_addr == '':
                            current_addr = get_cert_current_addr(words, phrase_list, i, window_size)
                        if permanent_addr == '':
                            permanent_addr = get_cert_permanent_addr(words, phrase_list, i, window_size)
                        if shown == '':
                            shown = get_cert_shown(words, phrase_list, i, window_size)
                        if wealth == '':
                            wealth = get_cert_wealth(words, phrase_list, i, window_size)
                        if paid == '':
                            paid = get_cert_paid(words, phrase_list, i, window_size)

                    # add to store
                    store[p.name]['cert_name'] = name
                    store[p.name]['cert_tin'] = tin
                    store[p.name]['cert_father'] = father
                    store[p.name]['cert_mother'] = mother
                    store[p.name]['cert_current_addr'] = current_addr
                    store[p.name]['cert_permanent_addr'] = permanent_addr
                    store[p.name]['cert_shown'] = shown
                    store[p.name]['cert_wealth'] = wealth
                    store[p.name]['cert_paid'] = paid

            # extract from slip page
            if p.name in slip_files:
                with open(join(dir_slip.absolute(), p.name), 'r') as f:
                    text = f.read().replace('\n', ' ').lower()
                    words_raw = text.split(' ')
                    words = filter_words(words_raw)
                    window_size = 5

                    name = ''
                    nid = ''
                    shown = ''
                    paid = ''

                    for i, word in enumerate(words):
                        # sliding window
                        phrase_list = words[i:min(i+window_size, len(words))]

                        if name == '':
                            name = get_slip_name(words, phrase_list, i, window_size)
                        if nid == '':
                            nid = get_slip_nid(words, phrase_list, i, window_size)
                        if shown == '':
                            shown = get_slip_shown(words, phrase_list, i, window_size)
                        if paid == '':
                            paid = get_slip_paid(words, phrase_list, i, window_size)

                    # add to store
                    store[p.name]['slip_name'] = name
                    store[p.name]['slip_nid'] = nid
                    store[p.name]['slip_shown'] = shown
                    store[p.name]['slip_paid'] = paid

            # extract from full text
            with open(join(directory.absolute(), p.name), 'r') as f:
                text = f.read().replace('\n', ' ').lower()
                words_raw = text.split(' ')
                words = filter_words(words_raw)
                window_size = 5

                text_data = {
                    'name': '',
                    'tin': '',
                    'nid': '',
                    'father': '',
                    'mother': '',
                    'shown': '',
                    'paid': '',
                    'wealth': '',
                    'claim': '',
                    'taxable': '',
                }

                phrase_text_data = {
                    'name': ['taxpayer', 'name'],
                    'tin': ['identification', 'number', 'tin'],
                    'nid': ['national', 'passport', 'nid'],
                    'father': ['father', 'name'],
                    'mother': ['mother', 'name'],
                    'shown': ['income', 'shown'],
                    'paid': ['tax', 'paid'],
                    'wealth': ['net', 'wealth'],
                    'claim': ['claimed', 'amount'],
                    'taxable': ['taxable', 'amount'],
                }                

                for i, word in enumerate(words):
                    # sliding window
                    phrase_list = words[i:min(i+window_size, len(words))]

                    for item, value in text_data.items():
                        if value == '':
                            item_phrase_list = phrase_text_data[item]
                            value = get_text_data(words, phrase_list, item_phrase_list, i)
                            if value != '':
                                text_data[item] = value
                                break

                # add to store
                for item, value in text_data.items():
                    store[p.name][f'text_{item}'] = value

        except Exception as e:
            print(p.name)
            print(e)
            continue
    
with open('data/store-alternative.json', 'w', encoding='utf8') as f:
    json.dump(store, f)