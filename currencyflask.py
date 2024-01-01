from flask import Flask, render_template, request
from datetime import date
import requests, re, datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("form.html")

    basecurrencyamt = float(request.form.get("amt"))
    baseunit = request.form["unit"]
    currtoconvert = request.form.get("currency to convert to")
    histconversionlst = []

    # basecurrencyamt = re.search(r'[\d.]+', amtandunit)
    # basecurrencyamt = float(basecurrencyamt.group())
    # baseunit = re.search(r'[a-zA-Z]+', amtandunit)
    # baseunit = baseunit.group()

    baseunit = baseunit.upper()
    currtoconvert = currtoconvert.upper()

    conversionurl = 'https://api.freecurrencyapi.com/v1/latest'
    histurl = "https://api.freecurrencyapi.com/v1/historical"
    
    conversionresponse = requests.get(conversionurl, params={"apikey":"fca_live_qvd2XQtgRAOIxbp9H8qIx0DEq5ZngipCkJmRWFsv", "base_currency":baseunit, "currencies":currtoconvert})
    responsedict = conversionresponse.json()
    conversionrate = responsedict["data"][currtoconvert]
    converted = str(round(conversionrate * basecurrencyamt, 2)) + " " + currtoconvert

    num_of_dates = 5
    start = datetime.datetime.today() - datetime.timedelta(days=1)
    date_list = [(start.date() - datetime.timedelta(days=x*365)).strftime('%Y-%m-%d') for x in range(num_of_dates)]
    print(date_list)
    for date in date_list:
        historicresponse = requests.get(histurl, params={"apikey":"fca_live_qvd2XQtgRAOIxbp9H8qIx0DEq5ZngipCkJmRWFsv", "date":date, "base_currency":baseunit, "currencies":currtoconvert})
        historicresponsedict = historicresponse.json()
        print(historicresponsedict)
        histconversion = historicresponsedict["data"][date][currtoconvert]
        histconversionlst.append((date, histconversion))
    print(histconversionlst)
    return render_template('form.html', convertedcurr=converted)

if __name__ == "__main__":
    app.run()