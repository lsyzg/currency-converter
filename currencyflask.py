from flask import Flask, render_template, request
import requests, json, re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("form.html")
    amtandunit = request.form.get("amtandunit")
    currtoconvert = request.form.get("currency to convert to")
    currtoconvert = currtoconvert.upper()

    basecurrencyamt = re.search(r'[\d.]+', amtandunit)
    basecurrencyamt = float(basecurrencyamt.group())
    baseunit = re.search(r'[a-zA-Z]+', amtandunit)
    baseunit = baseunit.group()
    baseunit = baseunit.upper()

    url = 'https://api.freecurrencyapi.com/v1/latest'
    response = requests.get(url, params={"apikey":"fca_live_qvd2XQtgRAOIxbp9H8qIx0DEq5ZngipCkJmRWFsv", "base_currency":baseunit, "currencies":currtoconvert})
    
    responsedict = response.json()
    conversionrate = responsedict["data"][currtoconvert]

    converted = str(round(conversionrate * basecurrencyamt, 2)) + " " + currtoconvert
    return render_template('form.html', convertedcurr=converted)

if __name__ == "__main__":
    app.run()