from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen, Request
from collections import defaultdict

app = Flask(__name__)

# ----------------------------
# PAGE D'ACCUEIL
# ----------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')


# ----------------------------
# EXERCICE 5 : PAGE CONTACT
# ----------------------------
@app.route("/contact/")
def contact():
    return render_template("contact.html")


# ----------------------------
# EXERCICE 3 : API METEO TAWARANO (JSON)
# ----------------------------
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin -> °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)


# ----------------------------
# EXERCICE 3 BIS / TER : PAGE GRAPHIQUE (LINECHART)
# ----------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# ----------------------------
# EXERCICE 4 : HISTOGRAMME TEMPÉRATURES
# ----------------------------
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")


# ----------------------------
# EXERCICE 6 : API COMMITS (agrégés par minute)
# ----------------------------
@app.route("/commits-data/")
def commits_data():
    # ⚠️ IMPORTANT : remplace OpenRSI/5MCSI_Metriques par TON repo fork
    # Exemple : "TonPseudo/5MCSI_Metriques"
    api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits?per_page=100"

    req = Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(req)
    raw_content = response.read()
    commits_json = json.loads(raw_content.decode("utf-8"))

    counts = defaultdict(int)

    for c in commits_json:
        # Chemin : commit -> author -> date
        date_string = c.get("commit", {}).get("author", {}).get("date")
        if not date_string:
            continue

        dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minute_key = dt.strftime("%Y-%m-%d %H:%M")  # regroupement par minute
        counts[minute_key] += 1

    results = [{"minute": k, "count": counts[k]} for k in sorted(counts.keys())]
    return jsonify(results=results)


# ----------------------------
# EXERCICE 6 : PAGE GRAPHIQUE COMMITS
# ----------------------------
@app.route("/commits/")
def commits_page():
    return render_template("commits.html")


if __name__ == "__main__":
    app.run(debug=True)
