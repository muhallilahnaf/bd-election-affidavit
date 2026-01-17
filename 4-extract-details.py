from pathlib import Path
from os.path import join
import json
from tqdm import tqdm


# folder paths
directory = Path("data/text/ereturn")
dir_cert = Path("data/text/ereturn/certificate")
dir_slip = Path("data/text/ereturn/slip")

# list of certificate and ereturn slip files
certificate_files = [p.name for p in dir_cert.iterdir()]
slip_files = [p.name for p in dir_slip.iterdir()]

# store data
store = {}

for p in tqdm(list(directory.iterdir())):
    if p.is_file():
        try:
            store[p.name] = {}
            # extract from certificate page
            if p.name in certificate_files:
                with open(join(dir_cert.absolute(), p.name), 'r') as f:
                    lines = f.readlines()
                    
                    name = ''
                    tin = ''
                    father = ''
                    mother = ''
                    current_addr = ''
                    permanent_addr = ''
                    summary = ''
                    
                    current_idx = None
                    permanent_idx = None
                    status_idx = None
                    shown_idx = None
                    system_idx = None
                    
                    for i, line in enumerate(lines):
                        line = line.lower()
                        # name
                        if all(['taxpayer' in line, 'name' in line, ':' in line]):
                            if name == '':
                                start = line.index(':')
                                name = line[start+1:].strip()
                                continue
                        # tin
                        if 'identification' in line and ':' in line:
                            if tin == '':
                                start = line.index(':')
                                tin = line[start+1:].strip()
                                continue
                        # father
                        if 'father' in line and ':' in line:
                            if father == '':
                                start = line.index(':')
                                father = line[start+1:].strip()
                                continue
                        # mother
                        if 'mother' in line and ':' in line:
                            if mother == '':
                                start = line.index(':')
                                mother = line[start+1:].strip()
                                continue
                        # current address
                        if 'current' in line and ':' in line:
                            if not current_idx:
                                current_idx = i
                                continue
                        # permanent address
                        if 'permanent' in line and ':' in line:
                            if not permanent_idx:
                                permanent_idx = i
                                continue
                        # ending line for permanent address
                        if 'status' in line and ':' in line:
                            if not status_idx:
                                status_idx = i
                                continue
                        # starting line for summary
                        if 'shown' in line:
                            if not shown_idx:
                                shown_idx = i
                                continue
                        # ending line for summary
                        if 'system' in line:
                            if not system_idx:
                                system_idx = i
                                continue
                    # get current address, permanent address and summary from lines
                    if current_idx and permanent_idx:
                        current_addr = " ".join(" ".join(lines[current_idx: permanent_idx]).split())
                    if permanent_idx and status_idx:
                        permanent_addr = " ".join(" ".join(lines[permanent_idx: status_idx]).split())
                    if shown_idx and system_idx:
                        summary = " ".join(" ".join(lines[shown_idx: system_idx]).split())

                    # add to store
                    store[p.name]['cert_name'] = name
                    store[p.name]['cert_tin'] = tin
                    store[p.name]['cert_father'] = father
                    store[p.name]['cert_mother'] = mother
                    store[p.name]['cert_current_addr'] = current_addr
                    store[p.name]['cert_permanent_addr'] = permanent_addr
                    store[p.name]['cert_summary'] = summary
            
            # extract from ereturn slip page
            if p.name in slip_files:
                with open(join(dir_slip.absolute(), p.name), 'r') as f:
                    lines = f.readlines()
                    
                    name = ''
                    nid = ''
                    shown = ''
                    paid = ''
                    
                    for line in lines:
                        line = line.lower()
                        # name
                        if all(['taxpayer' in line, 'name' in line, ':' in line]):
                            if name == '':
                                start = line.index(':')
                                name = line[start+1:].strip()
                                continue
                        # nid
                        if 'nid' in line and ':' in line:
                            if nid == '':
                                start = line.index(':')
                                nid = line[start+1:].strip()
                                continue
                        # income shown
                        if 'shown' in line and ':' in line:
                            if shown == '':
                                start = line.index(':')
                                shown = line[start+1:].strip()
                                continue
                        # tax paid
                        if 'paid' in line and ':' in line:
                            if paid == '':
                                start = line.index(':')
                                paid = line[start+1:].strip()
                                continue
                    
                    # add to store
                    store[p.name]['slip_name'] = name
                    store[p.name]['slip_nid'] = nid
                    store[p.name]['slip_shown'] = shown
                    store[p.name]['slip_paid'] = paid

            # extract from full text
            with open(join(directory.absolute(), p.name), 'r') as f:
                lines = f.readlines()

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
                    # name
                    if all([name == '', 'name' in line, ':' in line]):
                        if name == '':
                            start = line.index(':')
                            name = line[start+1:].strip()
                            continue
                    # tin
                    if 'tin' in line and ':' in line:
                        if tin == '':
                            start = line.index(':')
                            tin = line[start+1:].strip()
                            continue
                    # father
                    if 'father' in line and ':' in line:
                        if father == '':
                            start = line.index(':')
                            father = line[start+1:].strip()
                            continue
                    # mother
                    if 'mother' in line and ':' in line:
                        if mother == '':
                            start = line.index(':')
                            mother = line[start+1:].strip()
                            continue
                    # current address
                    if 'current' in line and ':' in line:
                        if current_addr == '':
                            current_addr = " ".join(" ".join(lines[i:i+3]).split())
                            continue
                    # permanent address
                    if 'permanent' in line and ':' in line:
                        if permanent_addr == '':
                            permanent_addr = " ".join(" ".join(lines[i:i+3]).split())
                            continue
                    # income shown
                    if 'shown' in line:
                        if shown == '':
                            shown = line
                            continue
                    # tax paid
                    if 'paid' in line:
                        if paid == '':
                            paid = line
                            continue
                    # net income
                    if 'net income' in line:
                        if net_income == '':
                            net_income = line
                            continue
                
                # add to store
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
    
# save store as json
with open('data/store.json', 'w', encoding='utf8') as f:
    json.dump(store, f)