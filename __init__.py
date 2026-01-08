from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')#comm3


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})
@app.route("/commits-data/")
def commits_data():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # GitHub aime bien un User-Agent
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(req)
    raw = response.read()
    commits_json = json.loads(raw.decode("utf-8"))

    # Compteur minutes 0..59
    counts = {m: 0 for m in range(60)}

    for c in commits_json:
        date_string = c.get("commit", {}).get("author", {}).get("date")
        if not date_string:
            continue

        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_object.minute
        counts[minute] += 1

    results = [{"minute": m, "count": counts[m]} for m in range(60)]
    return jsonify(results=results)


if __name__ == "__main__":
  app.run(debug=True)
