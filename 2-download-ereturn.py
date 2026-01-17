from playwright.sync_api import sync_playwright
import pandas as pd
from time import sleep
from pathlib import Path


# get list of all ereturn filenames
def get_all_filenames():
    directory = Path("data/ereturn")
    filenames = [p.name for p in directory.iterdir() if p.is_file()]
    return filenames


# get filename in format zillaID,constituencyID,candidate_name.pdf
def get_filename(row):
    return f"{row['zillaID']},{row['constituencyID']},{row['name']}.pdf"


# start playwright session
with sync_playwright() as p:
    count = 20

    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True, ignore_https_errors=True)
    page = context.new_page()

    filenames = get_all_filenames()
    df = pd.read_csv('data/candidates.csv')
    for _, row in df.iterrows():
        if count == 0:
            break
        name = row['name']
        # print(name)
        filename = get_filename(row)
        if filename not in filenames:
            ereturn = row['tax_return']
            if '|' in ereturn:
                url = ereturn.split('|')[1].strip()
                print('fetching ', name)
                response = page.request.get(url)
                with open(f"data/ereturn/{filename}", "wb") as f:
                    f.write(response.body())
                    count = count - 1
                sleep(2)
    browser.close()
