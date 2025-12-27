import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
FILE = Path("Baza leadova PI.xlsx")


def scrape_company(url: str) -> dict:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    container = soup.find("div", class_="rezultati")

    if not container:
        raise ValueError("Ne mogu da nađem glavni div: .rezulati.single_imenik")

    data = {
        "Naziv Firme": None,
        "E-mail": None,
        "Sajt": None,
        "PIB": None,
        "Matični broj": None,
        "informacije": None,
    }

    # Naziv firme
    title = container.select_one("h2.title")
    if title:
        data["Naziv Firme"] = title.get_text(strip=True)

    # Adresa + opis (prvi "description" blok sadrži dosta teksta)
    desc = container.select_one("div.jobs-item.with-big-thumb > div.description")
    if desc:
        # očisti whitespace, sačuvaj kao jedan string
        data["informacije"] = " ".join(desc.get_text(" ", strip=True).split())

    # E-mail i sajt (tražimo po labeli u levoj koloni)
    for row in container.select("div.row"):
        cols = row.select("div")
        if len(cols) < 2:
            continue

        label = cols[0].get_text(" ", strip=True).rstrip(":").lower()
        value_col = cols[1]

        if label == "e-mail":
            a = value_col.select_one('a[href^="mailto:"]')
            if a:
                data["E-mail"] = a.get_text(strip=True)

        elif label == "sajt":
            a = value_col.select_one('a[href]')
            if a:
                data["Sajt"] = a.get_text(strip=True)

    # PIB i Matični broj su u istom row-u (4 kolone: label, value, label, value)
    pib_label = container.find(string=lambda s: s and "PIB" in s)
    if pib_label:
        pib_value = pib_label.find_parent().find_next_sibling()
        if pib_value:
            data["PIB"] = pib_value.get_text(strip=True)

    mb_label = container.find(string=lambda s: s and "Matični broj" in s)
    if mb_label:
        mb_value = mb_label.find_parent().find_next_sibling()
        if mb_value:
            data["Matični broj"] = mb_value.get_text(strip=True)


    return data


if __name__ == "__main__":
    url = "https://www.privredni-imenik.com/Imenik/ROTOR-29447"  # primer
    company_data=scrape_company(url)
    print(company_data)

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