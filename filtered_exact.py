import pandas as pd

# Učitaj fajl
orig = pd.read_excel("DEAD END.xlsx")

# Filtriraj Status tako da bude tačno "ONLY MAIL"
filtered = orig[orig["Status"].astype(str).str.strip() == "ONLY MAIL"]

# Sačuvaj rezultat
filtered.to_excel("filtered_ONLY_MAIL_exact.xlsx", index=False)

print("Gotovo! Ukupno redova:", len(filtered))