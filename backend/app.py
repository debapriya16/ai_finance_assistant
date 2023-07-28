import json
from flask import Flask, request, jsonify
from utils import Offer, read_datasets, get_customer_details, get_investment_categories

app = Flask(__name__)

@app.route("/alive")
def check_app():
    return "<p>I am alive!</p>"


@app.route('/offers/<cust_id>', methods=['GET'])
def cust_offers(cust_id):
    df, df1 = read_datasets('../dataset/account-statement.csv', '../dataset/Bank_Customer_Details.csv')
    cust_details = get_customer_details(df1, int(cust_id))
    offer = Offer(cust_details)
    scheme = offer.check_age_offers()
    return jsonify(scheme)


@app.route('/transaction/categories/<cust_id>', methods=['GET'])
def cust_transaction_categories(cust_id):
    df, df1 = read_datasets('../dataset/account-statement.csv', '../dataset/Bank_Customer_Details.csv')
    buckets = get_investment_categories(df)
    return jsonify(buckets.to_dict())


@app.route('/customer/<cust_id>', methods=['GET'])
def cust_details(cust_id):
    df, df1 = read_datasets('../dataset/account-statement.csv', '../dataset/Bank_Customer_Details.csv')
    cust_details = get_customer_details(df1, int(cust_id))
    return jsonify(cust_details.to_dict())


if __name__ == "__main__":
    app.run(debug=True)