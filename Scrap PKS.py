import requests
from bs4 import BeautifulSoup

root_url = "https://www.privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=432100"

response = requests.get(root_url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Nađi spoljašnji div sa klasom "rezulati"
results_div = soup.find("div", class_="rezultati")

# Svi <a> tagovi unutar tog diva
company_links = results_div.select("div.jobs-item h6.title a")

for a in company_links:
    print(a.get("href"), "->", a.get_text(strip=True))