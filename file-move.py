from pathlib import Path
import os
import shutil

# 
# split all pdf files to 2 sets for 2 computers  
# 


count = 1500

directory = Path("data/ereturn")
for p in directory.iterdir():
    if count == 0:
        break
    if os.path.exists(f'data/text/ereturn/{p.name.replace(".pdf", "")}.txt'):
        continue
    else:
        shutil.move(f'data/ereturn/{p.name}', f'data/ereturnp2/{p.name}')
        count -= 1



