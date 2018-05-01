# -*- coding: utf-8 -*-
# -*- File: app.py -*-
# -*- Author: aB9 -*-
# -*- Date: 03/12 -*-

import cryptocompare
import datetime
import flask
from flask import Flask, render_template, jsonify
import requests
import ObjCryptoCurrency
import json

# quandl.ApiConfig.api_key = '9JgSrLaxsP64AhdQ6Ss9'

import os
import json
import pandas as pd
import csv
import numpy as np
import datetime
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,10)

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm



app = Flask(__name__)

# From CryptoCurrency Object
CrCurrency = ObjCryptoCurrency.CryptoCurrency
CrCurrencyDetails = ObjCryptoCurrency.CryptoCurrencyDetails
crc_dict = ObjCryptoCurrency.cryptocurrencies_dict
crc_list = ObjCryptoCurrency.cryptocurrencies_list


# List to store CryptoCurrency data fetched from the server
cryptocurrencies_data = []

currency = []
currency1 = []
currency2 = []
forecast_prediction = []


# Index.html page
@app.route("/")
def index():
    return render_template('index.html')

# Get list of Cryptocurrencies
@app.route('/cryptocurrency_list', methods=['GET'])
def getCrycptoCurrencyList():
    try:
        list_ = cryptocompare.get_coin_list(format=False)
        print(type(list_))
        print(list_)
        list_string = json.dumps(list_)
        cr_list_json = json.loads((list_string))
        print(type(cr_list_json))
        print(cr_list_json)
        CrCurrencyList = []
        for key, value in sorted(cr_list_json.items()):
            if key in crc_list:
                print(key)
                print(value)
                CrCurrencyList.append(CrCurrency(name=value['CoinName'], symbol=value['Symbol'],url=value['Url'], image_url=value['ImageUrl']))

        for cr in CrCurrencyList:
            print(cr)

            return jsonify({'status': 'success'}, json.dumps([ob.__dict__ for ob in CrCurrencyList]))
    except Exception as e:
        return jsonify({'status': 'failed'})

@app.route("/currency_meta_data", methods=["GET"])
def getCryptoCurrencyList():
    cr_id = (flask.request.args).to_dict(flat=False)["cr_id"][0]
    try:
        cryptocurrencies_data = []
        # URL to get current price data
        # URL = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(cr_id)
        URL = 'https://min-api.cryptocompare.com/data/generateAvg?fsym={}&tsym=USD&e=CCCAGG'.format(cr_id)
        response = requests.get(URL)
        # Request successful
        if response.status_code == 200:
            json_response = response.json()
            # store data into cryptocurrency_data list
            # if json_response['Response'] == 'Success':
            data = json_response['DISPLAY']

            currency = CrCurrency(asset_id=cr_id, cr_price=data['PRICE'], cr_last_vol_to=data['LASTVOLUMETO'],cr_vol_24_hr=data['VOLUME24HOUR'],cr_open_24_hr=data['OPEN24HOUR'],cr_high_24_hr=data['HIGH24HOUR'],
                              cr_low_24_hr=data['LOW24HOUR'],cr_change_24_hr=data['CHANGE24HOUR'])

            # return jsonify({'status': 'success'}, json.dumps([ob.__dict__ for ob in currency]))
            return jsonify({'status': 'success'}, currency.toJSON())
        else:
            return jsonify({'status': 'failed'})
    except Exception as e:
        return jsonify({'status': 'failed'})


# CryptoCurrency_in_details.html page
# noinspection PyUnreachableCode
@app.route("/<cryptocurrency_asset_id>")
def cryptocurrency_in_details(cryptocurrency_asset_id):
    currency = CrCurrency()
    currency1 = CrCurrency()
    currency2 = CrCurrency()
    #    currency_details = CrCurrencyDetails()
    currency_name = ""
    for c_name, c_id in crc_dict.items():
        if c_id == cryptocurrency_asset_id:
            currency_name = c_name

            # URL to get cryptocurrency data in detail
    URL = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(
        cryptocurrency_asset_id)
    response = requests.get(URL)

    # Request successful
    if response.status_code == 200:
        json_response = response.json()
        # store data into cryptocurrency_data list
        if json_response['Response'] == 'Success':
            data = json_response['Data'][0]
            currency = CrCurrency(cryptocurrency_asset_id, currency_name, data['time'], data['close'], data['high'],
                                  data['low'], data['open'], data['volumefrom'], data['volumeto'])

        else:
            return render_template('error_page.html')
    # Error occurred
    else:
        return render_template('error_page.html')



    URL = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(
        cryptocurrency_asset_id)
    response = requests.get(URL)

    # Request successful
    if response.status_code == 200:
        json_response = response.json()
        # store data into cryptocurrency_data list
        if json_response['Response'] == 'Success':
            data = json_response['Data'][0]
            currency1 = CrCurrency(cryptocurrency_asset_id, currency_name, data['time'], data['close'], data['high'],
                                  data['low'], data['open'], data['volumefrom'], data['volumeto'])

        else:
            return render_template('error_page.html')
    # Error occurred
    else:
        return render_template('error_page.html')

    URL = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&limit=1&aggregate=3&e=CCCAGG'.format(
        cryptocurrency_asset_id)
    response = requests.get(URL)

    # Request successful
    if response.status_code == 200:
        json_response = response.json()
        # store data into cryptocurrency_data list
        if json_response['Response'] == 'Success':
            data = json_response['Data'][0]
            currency2 = CrCurrency(cryptocurrency_asset_id, currency_name, data['time'], data['close'], data['high'],
                                   data['low'], data['open'], data['volumefrom'], data['volumeto'])

        else:
            return render_template('error_page.html')
    # Error occurred
    else:
        return render_template('error_page.html')

    return render_template('cryptocurrency_in_details.html', currency1=currency1 , currency = currency , currency2 = currency2)


@app.route('/news', methods=["GET"])
def news():
    # name = Flask.request_class.args.get('name',default=None, type=None)
    try:
        asset_id = (flask.request.args).to_dict(flat=False)["asset_id"][0]
        currency_name = ""
        for c_name, c_id in crc_dict.items():
            if c_id == asset_id:
                currency_name = c_name

        URL = 'https://newsapi.org/v2/everything?q={}&sortBy=publishedAt&apiKey=3fabdc3fed8d481c92f7c2deeb0147e9'.format(
            currency_name)
        response = requests.get(URL)

        # Request successful
        if response.status_code == 200:
            json_response = response.json()
            print(json_response)
            return jsonify({'status': 'success'}, json_response)

        # Error occurred
        else:
            return jsonify({'status': 'error'})

    except Exception as e:
        return jsonify({'status': 'error'})


@app.route('/market_details', methods=["GET"])
def market_details():
    # name = Flask.request_class.args.get('name',default=None, type=None)

    asset_id = (flask.request.args).to_dict(flat=False)["asset_id"][0]
    # currency_details = CrCurrencyDetails()
    # URL to get cryptocurrency data in detail
    URL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD'.format(asset_id)
    response = requests.get(URL)

    # Request successful
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
        return jsonify({'status': 'success'}, json_response)

    # Error occurred
    else:
        return jsonify({'status': 'error'})


@app.route('/multiple_symbol_price', methods=["GET"])
def getMultiplePrices():
    # name = Flask.request_class.args.get('name',default=None, type=None)

    asset_id = (flask.request.args).to_dict(flat=False)["asset_id"][0]
    # currency_details = CrCurrencyDetails()
    # URL to get cryptocurrency data in detail
    URL = 'https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms=USD,EUR,INR,AUD,AED'.format(asset_id)
    response = requests.get(URL)

    # Request successful
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
        return jsonify({'status': 'success'}, json_response)

    # Error occurred
    else:
        return jsonify({'status': 'error'})

# @app.route('/prediction', methods=["GET"])
# def prediction():
#     df = quandl.get("BCHARTS/KRAKENUSD", start_date="2018-01-01", end_date="2018-03-10")
#     df = df[['Close']]
#
#     forecast_out = int(7)  # predicting 7 days into future
#     df['Prediction'] = df.shift(-forecast_out)  # label column with data shifted 7 units up
#
#     X = np.array(df.drop(['Prediction'], 1))
#     X = preprocessing.scale(X)
#
#     X_forecast = X[-forecast_out:]  # set X_forecast equal to last 30
#     X = X[:-forecast_out]  # remove last 7 from X
#
#     y = np.array(df['Prediction'])
#     y = y[:-forecast_out]
#
#     X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
#
#     # Training
#     clf = LinearRegression()
#     clf.fit(X_train, y_train)
#     # Testing
#     confidence = clf.score(X_test, y_test)
#     print("confidence: ", confidence)
#
#     forecast_prediction = clf.predict(X_forecast)
#     print(forecast_prediction)
#     for i in forecast_prediction:
#         print(i)
#         forecast_prediction[i] = float("%3.f" % forecast_prediction)
#
#     print(forecast_prediction)
#
#     forecast_with_dates = {}
#     for i in range(0, 7):
#         _date = datetime.datetime.now() + datetime.timedelta(days=(i + 1))
#         forecast_with_dates[_date.timestamp()] = forecast_prediction[i]
#
#     print(forecast_with_dates)
#
#     return jsonify(forecast_with_dates)


@app.route('/prediction', methods=["GET"])
def prediction():
    # Get Live data from the server
    try:
        crycpto_currency = (flask.request.args).to_dict(flat=False)["asset_id"][0]
        URL = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym=USD&limit=1000&aggregate=3&e=CCCAGG'.format(crycpto_currency)
        #     URL = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym=USD&limit=10000'.format(crycpto_currency)
        response = requests.get(URL)
        if response.status_code == 200:
            json_response = response.json()
            crc_data = json_response['Data']
            print(crc_data)
        else:
            print("Error")


        # Convert json data to the CSV
        filename = 'crc_day_history.csv'
        try:
            os.remove(filename)
        except OSError:
            pass
        # Open a file for writing
        crypto_currency_data = open(filename, 'w')

        # Create a csv writter object
        csvwritter = csv.writer(crypto_currency_data)

        count = 0

        for cr in crc_data:
            if count == 0:
                header = cr.keys()
                csvwritter.writerow(header)
                count += 1
            csvwritter.writerow(cr.values())

        crypto_currency_data.close()

        # Reading CSV file
        crypto_currency_file = open('crc_day_history.csv','r')
        crypto_currency_csv = csv.reader(crypto_currency_file)

        # for row in crypto_currency_csv:
        #     print(row)

        crypto_pd_obj = pd.read_csv(filename)

        # Plot the graph of all data
        crypto_pd_obj.plot()

        crc_pred = crypto_pd_obj[['open', 'close']]
        print(crc_pred.tail())

        crc_pred.plot()

        forecast_out = int(1)  # predicting 1 day into future
        crc_pred['Prediction'] = crc_pred[['open']].shift(-forecast_out)  # label column with data shifted 1 units up

        X = np.array(crc_pred.drop(['Prediction'], 1))
        X = preprocessing.scale(X)

        X_forecast = X[-forecast_out:]  # set X_forecast equal to last 1
        X = X[:-forecast_out]  # remove last 30 from X

        y = np.array(crc_pred['Prediction'])
        y = y[:-forecast_out]

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

        clf = LinearRegression()
        clf.fit(X_train, y_train)

        confidence = clf.score(X_test, y_test)
        print("confidence: ", confidence)

        forecast_prediction = clf.predict(X_forecast)
        print(forecast_prediction)

        # pd.DataFrame(forecast_prediction).plot(color="blue")
        pred_list = forecast_prediction.tolist()
        print(pred_list[0])

        # for i in forecast_prediction:
        #     print(i)
        #     forecast_prediction[i] = float("%3.f" % forecast_prediction)
        #
        #
        # forecast_with_dates = {}
        # for i in range(0, 7):
        #     _date = datetime.datetime.now() + datetime.timedelta(days=(i + 1))
        #     forecast_with_dates[_date.timestamp()] = forecast_prediction[i]
        #
        # print(forecast_with_dates)

        # return jsonify(forecast_prediction)
        return jsonify({'status': 'error'}, {'prediction':float(("%0.2f"%pred_list[0]))})

    except Exception as e:
        print("Error")



if __name__ == "__main__":
    app.run()
