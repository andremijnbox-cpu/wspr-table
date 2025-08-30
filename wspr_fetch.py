import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
    <title>WSPR Tabel</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 6px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>WSPR Tabel</h1>
    <p>Laatste update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

# Zoek en verwerk de tabel
if soup:
    pre = soup.find("pre")
    if pre:
        lines = pre.text.strip().split("\n")
        html += "<table>\n<tr>"
        headers = [h.strip() for h in lines[2].split("|") if h.strip()]
        for h in headers:
            html += f"<th>{h}</th>"
        html += "</tr>\n"

        for line in lines[4:14]:  # Pak de eerste 10 spots
            cells = [c.strip() for c in line.split("|") if c.strip()]
            html += "<tr>"
            for cell in cells:
                html += f"<td>{cell}</td>"
            html += "</tr>\n"
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
