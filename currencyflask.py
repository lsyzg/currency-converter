from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("form.html")
    amtandtype = request.form.get("amtandtype")
    currtoconvert = request.form.get("currency to convert to")
    currtoconvert = currtoconvert.upper()

    mylist = list(amtandtype)
    # basecurrencyamt = int(''.join([x for x in list(filter(None, mylist)) if isinstance(x, int)]))
    # baseunit = (''.join([x for x in mylist if isinstance(x, str)])).upper()

    baseunit = request.form.get("unit")
    baseunit = baseunit.upper()
    basecurrencyamt = float(amtandtype)

    url = 'https://api.freecurrencyapi.com/v1/latest'
    response = requests.get(url, params={"apikey":"fca_live_qvd2XQtgRAOIxbp9H8qIx0DEq5ZngipCkJmRWFsv", "base_currency":baseunit, "currencies":currtoconvert})
    
    conversionratedict = response.json()
    currencydict = conversionratedict["data"]
    conversionrate = currencydict[currtoconvert]
    
    converted = round(conversionrate * basecurrencyamt, 2)
    return render_template('form.html', convertedcurr=converted)

if __name__ == "__main__":
    app.run()