import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re  # Verplaatst naar boven

FILTER_CALLSIGN = "M0MBO"
URL = "https://www.wsprnet.org/drupal/wsprnet/spots"

try:
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
except Exception as e:
    print(f"⚠️ Fout bij ophalen data: {e}")
    soup = None

# HTML-header
html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WSPR Tabel voor {FILTER_CALLSIGN}</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 6px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>WSPR Tabel voor {FILTER_CALLSIGN}</h1>
    <p>Laatste update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

# Zoek en verwerk de tabel
if soup:
    pre = soup.find("pre")
    if pre:
        lines = pre.text.strip().split("\n")
        html += "<table>\n<tr>"
        headers = re.split(r'\s{2,}|\t+', lines[2].strip())
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>\n"

        count = 0
        for line in lines[4:]:
            cells = re.split(r'\s{2,}|\t+', line.strip())
            if len(cells) < 5:
                continue
            if cells[1] == FILTER_CALLSIGN:
                html += "<tr>"
                for cell in cells:
                    html += f"<td>{cell}</td>"
                html += "</tr>\n"
                count += 1
            if count >= 10:
                break

        if count == 0:
            html += f"<tr><td colspan='{len(headers)}'>⚠️ Geen spots gevonden voor {FILTER_CALLSIGN}</td></tr>\n"

        html += "</table>\n"
    else:
        html += "<p>⚠️ Geen spotdata gevonden.</p>"
else:
    html += "<p>⚠️ Fout bij ophalen van de pagina.</p>"

# HTML-footer
html += """
    <p>Deze pagina is automatisch gegenereerd door GitHub Actions.</p>
</body>
</html>
"""

# Schrijf naar index.html
with open("index.html", "w") as f:
    f.write(html)
