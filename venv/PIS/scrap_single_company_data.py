import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time
import random

FILE = Path("Baza leadova PI.xlsx")


def make_session() -> requests.Session:
    s = requests.Session()

    # 3) User-Agent header (+ par korisnih headera)
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept-Language": "sr-RS,sr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    })

    # 1) Timeout + retry (3 pokušaja) + backoff
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        status=3,
        backoff_factor=1.0,  # ~ 1s, 2s, 4s pauze između retry-a
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,  # da retry radi i kad je 429/5xx
    )

    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)

    return s


# napravi jednom i koristi svuda
SESSION = make_session()


def scrape_company(url: str, session: requests.Session = SESSION) -> dict:
    # 2) Sleep / rate-limit (random 1–3s)
    time.sleep(random.uniform(1, 3))

    # Timeout kao (connect_timeout, read_timeout)
    r = session.get(url, timeout=(5, 30))

    # Ako nije OK, baci grešku (posle retry pokušaja)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    container = soup.find("div", class_="rezultati")
    if not container:
        raise ValueError("Ne mogu da nađem glavni div: .rezultati")

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
        data["informacije"] = " ".join(desc.get_text(" ", strip=True).split())

    # E-mail i sajt
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

    # PIB
    pib_label = container.find(string=lambda s: s and "PIB" in s)
    if pib_label:
        pib_value = pib_label.find_parent().find_next_sibling()
        if pib_value:
            data["PIB"] = pib_value.get_text(strip=True)

    # Matični broj
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