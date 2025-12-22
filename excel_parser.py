import pandas as pd

# Učitaj originalni Excel
orig = pd.read_excel("DEAD END.xlsx")

# Filtriraj redove
filtered = orig[orig["Status"].astype(str).str.startswith("ONLY MAIL")]

# Sačuvaj novi Excel fajl
filtered.to_excel("filtered_ONLY MAIL.xlsx", index=False)

print("Excel fajl je uspešno napravljen!")