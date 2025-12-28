
import pandas as pd
from pathlib import Path
FILE = Path("Baza leadova PI.xlsx")

def write_data(company_data):

    row = {
        "names": company_data.get("Naziv Firme"),
        "Email": company_data.get("E-mail"),
        "MB": company_data.get("Matični broj"),
        "Izvor": "Privredni Imenik page",
    }

    df_new = pd.DataFrame([row])

    # UČITAJ postojeći Excel
    df_old = pd.read_excel(FILE)

    # APPEND (kolone se već poklapaju)
    df_all = pd.concat([df_old, df_new], ignore_index=True)

    df_all.to_excel(FILE, index=False)