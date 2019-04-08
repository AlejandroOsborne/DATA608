from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd
import os

app = Flask(__name__)

CSV_URL     = 'https://data.cityofnewyork.us/resource/uvpi-gqnh.json'
CSV_PATH    = 'data.csv'

def get_df():
    #If the data is already saved to disk
    if os.path.isfile(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    #If the data is not saved, download and save
    df = pd.read_json(CSV_URL)
    df.to_csv(CSV_PATH)
    return df

# This is an API meant to serve some housing price index data
@app.route('/tpi_html/<string:boroname>/<string:health>')
def to_html(boroname, health):

    df = get_df()

    df =  df[(df['boroname'] == boroname) & (df['health']== health)]
    return df.to_html()


# This is an API meant to serve some housing price index data
@app.route('/tpi_json/<string:boroname>/<string:health>')
def to_json(boroname, health):

    df = get_df()

    df =  df[(df['boroname'] == boroname) & (df['health']== health)]
    return df.to_json()


if __name__ == '__main__':
    app.run(debug=True)
