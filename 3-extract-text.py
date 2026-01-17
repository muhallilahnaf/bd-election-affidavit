from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from os.path import join
from difflib import SequenceMatcher
from tqdm import tqdm

# lib paths
poppler_path = "C:\\Users\\matus\\AppData\\Local\\Programs\\poppler-25.12.0\\Library\\bin"
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

count = 50

ereturn_slip_title = 'Acknowledgement Receipt/Certificate of Return of Income'
ereturn_cert_title = 'Income Tax Certificate'

# list of already extracted text files
filenames = [p.name.replace('.txt', '') for p in Path("data/text/ereturn").iterdir() if p.is_file()]

# pdf path
directory = Path("data/ereturn")
for p in directory.iterdir():
    if count == 0:
        break
    if p.is_file() and p.name.endswith('.pdf'):
        pdf_path = join(directory.absolute(), p.name)
        new_name = p.name.replace('.pdf', '')
        # if not already extracted
        if new_name not in filenames:
            print(new_name)
            # pdf to img
            pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
            fulltext = ""
            for page in tqdm(pages):
                # img to string
                text = pytesseract.image_to_string(page)
                # collect full text
                fulltext += text + '\n'
                lines = text.split('\n')
                for line in lines:
                    # ereturn slip page
                    if SequenceMatcher(None, line, ereturn_slip_title).ratio() > 0.80:
                        with open(f'data/text/ereturn/slip/{new_name}.txt', 'w') as f:
                            f.write(text)
                            break
                    # ereturn certificate page
                    if SequenceMatcher(None, line, ereturn_cert_title).ratio() > 0.80:
                        with open(f'data/text/ereturn/certificate/{new_name}.txt', 'w') as f:
                            f.write(text)
                            break
            with open(f'data/text/ereturn/{new_name}.txt', 'w') as f:
                f.write(fulltext)
            count = count - 1
            print(count, ' left')
