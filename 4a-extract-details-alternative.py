from pathlib import Path
from os.path import join
import json
from tqdm import tqdm
from rapidfuzz import fuzz
import re


directory = Path("data/text/ereturn")
dir_cert = Path("data/text/ereturn/certificate")
dir_slip = Path("data/text/ereturn/slip")

certificate_files = [p.name for p in dir_cert.iterdir()]
slip_files = [p.name for p in dir_slip.iterdir()]

store = {}

def get_cert_name(words, phrase, i):
    name = ''
    phrase_name = 'taxpayers name'
    ending_word = 'taxpayers'
    lookahead_size = 5
    ratio = fuzz.ratio(phrase, phrase_name)
    print(ratio)
    if ratio > 80:
        start = i + len(phrase_name.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            name = ' '.join(words[start:j])
    return name

def get_cert_tin(words, phrase, i):
    tin = ''
    phrase_tin = 'taxpayers identification number'
    ending_word = 'fathers'
    lookahead_size = 5
    if fuzz.ratio(phrase, phrase_tin) > 80:
        start = i + len(phrase_tin.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            tin = ' '.join(words[start:j])
        tin = re.sub(r'\D+', '', tin)
    return tin

def get_cert_father(words, phrase, i):
    father = ''
    phrase_father = 'fathers name'
    ending_word = 'mothers'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_father) > 80:
        start = i + len(phrase_father.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            father = ' '.join(words[start:j])
    return father

def get_cert_mother(words, phrase, i):
    mother = ''
    phrase_mother = 'mothers name'
    ending_word = 'current'
    lookahead_size = 10
    if fuzz.ratio(phrase, phrase_mother) > 80:
        start = i + len(phrase_mother.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            mother = ' '.join(words[start:j])
    return mother

def get_cert_current_addr(words, phrase, i):
    current_addr = ''
    phrase_current_addr = 'current address'
    ending_word = 'permanent'
    lookahead_size = 30
    if fuzz.ratio(phrase, phrase_current_addr) > 80:
        start = i + len(phrase_current_addr.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            current_addr = ' '.join(words[start:j])
    return current_addr

def get_cert_permanent_addr(words, phrase, i):
    permanent_addr = ''
    phrase_permanent_addr = 'permanent address'
    ending_word = 'status'
    lookahead_size = 30
    if fuzz.ratio(phrase, phrase_permanent_addr) > 80:
        start = i + len(phrase_permanent_addr.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            permanent_addr = ' '.join(words[start:j])
    return permanent_addr

def get_cert_shown(words, phrase, i):
    shown = ''
    phrase_shown = 'shown total income'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_shown) > 80:
        start = i + len(phrase_shown.split(' '))
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        shown = ' '.join(words[start:end])
        shown = re.sub(r'\D+', '', shown)
    return shown

def get_cert_wealth(words, phrase, i):
    wealth = ''
    phrase_wealth = 'net wealth'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_wealth) > 80:
        start = i + len(phrase_wealth.split(' '))
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        wealth = ' '.join(words[start:end])
        wealth = re.sub(r'\D+', '', wealth)
    return wealth

def get_cert_paid(words, phrase, i):
    paid = ''
    phrase_paid = 'paid tax'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_paid) > 80:
        start = i + len(phrase_paid.split(' '))
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        paid = ' '.join(words[start:end])
        paid = re.sub(r'\D+', '', paid)
    return paid

def get_slip_name(words, phrase, i):
    name = ''
    phrase_name = 'name of the taxpayer'
    ending_word = 'nid'
    lookahead_size = 5
    if fuzz.ratio(phrase, phrase_name) > 80:
        start = i + len(phrase_name.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            name = ' '.join(words[start:j])
    return name

def get_slip_nid(words, phrase, i):
    nid = ''
    phrase_nid = 'passport no if no nid'
    ending_word = 'circle'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_nid) > 80:
        start = i + len(phrase_nid.split(' '))
        j = None
        for j in range(start, min(i+lookahead_size, len(words))):
            if fuzz.ratio(words[j], ending_word) > 90:
                break
        if j:
            nid = ' '.join(words[start:j])
            nid = re.sub(r'\D+', '', nid)
    return nid

def get_slip_shown(words, phrase, i):
    shown = ''
    phrase_shown = 'total income shown'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_shown) > 80:
        start = i + len(phrase_shown.split(' '))
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        shown = ' '.join(words[start:end])
        shown = re.sub(r'\D+', '', shown)
    return shown

def get_slip_paid(words, phrase, i):
    paid = ''
    phrase_paid = 'total tax paid'
    lookahead_size = 3
    if fuzz.ratio(phrase, phrase_paid) > 80:
        start = i + len(phrase_paid.split(' '))
        if start+lookahead_size < len(words):
            end = start+lookahead_size
        else:
            end = len(words)
        paid = ' '.join(words[start:end])
        paid = re.sub(r'\D+', '', paid)
    return paid

count = 5

for p in tqdm(list(directory.iterdir())):
    count -= 1
    if p.is_file() and count == 0:
        try:
            store[p.name] = {}
            if p.name in certificate_files:
                with open(join(dir_cert.absolute(), p.name), 'r') as f:
                    text = f.read().replace('\n', ' ').lower()
                    words = text.split(' ')
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
                        if i+window_size < len(words):
                            phrase = ' '.join(words[i:i+window_size])
                        else:
                            phrase = ' '.join(words[i:])
                        if name == '':
                            name = get_cert_name(words, phrase, i)
                        if tin == '':
                            tin = get_cert_tin(words, phrase, i)
                        if father == '':
                            father = get_cert_father(words, phrase, i)
                        if mother == '':
                            mother = get_cert_mother(words, phrase, i)
                        if current_addr == '':
                            current_addr = get_cert_current_addr(words, phrase, i)
                        if permanent_addr == '':
                            permanent_addr = get_cert_permanent_addr(words, phrase, i)
                        if shown == '':
                            shown = get_cert_shown(words, phrase, i)
                        if wealth == '':
                            wealth = get_cert_wealth(words, phrase, i)
                        if paid == '':
                            paid = get_cert_paid(words, phrase, i)
                    store[p.name]['cert_name'] = name
                    store[p.name]['cert_tin'] = tin
                    store[p.name]['cert_father'] = father
                    store[p.name]['cert_mother'] = mother
                    store[p.name]['cert_current_addr'] = current_addr
                    store[p.name]['cert_permanent_addr'] = permanent_addr
                    store[p.name]['cert_shown'] = shown
                    store[p.name]['cert_wealth'] = wealth
                    store[p.name]['cert_paid'] = paid
            if p.name in slip_files:
                with open(join(dir_slip.absolute(), p.name), 'r') as f:
                    text = f.read().replace('\n', '').lower()
                    words = text.split(' ')
                    window_size = 4
                    name = ''
                    nid = ''
                    shown = ''
                    paid = ''
                    for i, word in enumerate(words):
                        if i+window_size < len(words):
                            phrase = ' '.join(words[i:i+window_size])
                        else:
                            phrase = ' '.join(words[i:])
                        if name == '':
                            name = get_slip_name(words, phrase, i)
                        if nid == '':
                            nid = get_slip_nid(words, phrase, i)
                        if shown == '':
                            shown = get_slip_shown(words, phrase, i)
                        if paid == '':
                            paid = get_slip_paid(words, phrase, i)
                    store[p.name]['slip_name'] = name
                    store[p.name]['slip_nid'] = nid
                    store[p.name]['slip_shown'] = shown
                    store[p.name]['slip_paid'] = paid
            with open(join(directory.absolute(), p.name), 'r') as f:
                lines = f.readlines()
                #print(lines)
                name = ''
                tin = ''
                father = ''
                mother = ''
                current_addr = ''
                permanent_addr = ''
                shown = ''
                paid = ''
                net_income  = ''
                for i, line in enumerate(lines):
                    line = line.lower()
                    if all([name == '', 'name' in line, ':' in line]):
                        if name == '':
                            start = line.index(':')
                            name = line[start+1:].strip()
                            continue
                    if 'tin' in line and ':' in line:
                        if tin == '':
                            start = line.index(':')
                            tin = line[start+1:].strip()
                            continue
                    if 'father' in line and ':' in line:
                        if father == '':
                            start = line.index(':')
                            father = line[start+1:].strip()
                            continue
                    if 'mother' in line and ':' in line:
                        if mother == '':
                            start = line.index(':')
                            mother = line[start+1:].strip()
                            continue
                    if 'current' in line and ':' in line:
                        if current_addr == '':
                            current_addr = " ".join(" ".join(lines[i:i+3]).split())
                            continue
                    if 'permanent' in line and ':' in line:
                        if permanent_addr == '':
                            permanent_addr = " ".join(" ".join(lines[i:i+3]).split())
                            continue
                    if 'shown' in line:
                        if shown == '':
                            shown = line
                            continue
                    if 'paid' in line:
                        if paid == '':
                            paid = line
                            continue
                    if 'net income' in line:
                        if net_income == '':
                            net_income = line
                            continue
                store[p.name]['text_name'] = name
                store[p.name]['text_tin'] = tin
                store[p.name]['text_father'] = father
                store[p.name]['text_mother'] = mother
                store[p.name]['text_current_addr'] = current_addr
                store[p.name]['text_permanent_addr'] = permanent_addr
                store[p.name]['text_shown'] = shown
                store[p.name]['text_paid'] = paid
                store[p.name]['text_net_income'] = net_income
        except Exception as e:
            print(p.name)
            print(e)
            continue
    
with open('data/store-alternative.json', 'w', encoding='utf8') as f:
    json.dump(store, f)