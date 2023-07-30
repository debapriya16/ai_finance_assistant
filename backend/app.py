import json
from flask import Flask, request, jsonify
from utils import Offer, read_datasets, get_customer_details, get_investment_categories
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


@api.route("/alive")
class CheckApp(Resource):
    def get(self):
        return "<p>I am alive!</p>"


@api.route('/offers/<cust_id>')
class CustOffers(Resource):
    def get(self, cust_id):
        df, df1 = read_datasets('../dataset/account-statement-{}.csv'.format(cust_id), '../dataset/Bank_Customer_Details.csv')
        cust_details = get_customer_details(df1, int(cust_id))
        offer = Offer(cust_details)
        age_scheme = offer.check_age_offers()
        preference_scheme = offer.check_customer_preferences(df)
        risk_scheme = offer.check_risk_analysis(cust_id)
        electoral_scheme = offer.electoral_offers()
        scheme = {}
        scheme.update(age_scheme)
        scheme.update(preference_scheme)
        if risk_scheme != "No Risk Detected":
            scheme.update(risk_scheme)
        if electoral_scheme != "No Voting Benefits found":
            scheme.update(electoral_scheme)
        return jsonify(scheme)


@api.route('/transaction/categories/<cust_id>')
class CustTransactionCategories(Resource):
    def get(self, cust_id):
        df, df1 = read_datasets('../dataset/account-statement-{}.csv'.format(cust_id), '../dataset/Bank_Customer_Details.csv')
        buckets = get_investment_categories(df)
        return jsonify(buckets.to_dict())


@api.route('/transaction/amount/<cust_id>')
class CustTransactionSum(Resource):
    def get(self, cust_id):
        df, df1 = read_datasets('../dataset/account-statement-{}.csv'.format(cust_id), '../dataset/Bank_Customer_Details.csv')
        # Use GroupBy() & compute sum on specific column
        buckets = df.groupby('Category')['Debit_Amount'].sum()
        return jsonify(buckets.to_dict())


@api.route('/customer/<cust_id>')
class CustDetails(Resource):
    def get(self, cust_id):
        df, df1 = read_datasets('../dataset/account-statement-{}.csv'.format(cust_id), '../dataset/Bank_Customer_Details.csv')
        cust_details = get_customer_details(df1, int(cust_id))
        return jsonify(cust_details.to_dict())


@api.route('/offers/seasonal/<cust_id>')
class CustSeasonOffers(Resource):
    def get(self,cust_id):
        df, df1 = read_datasets('../dataset/account-statement-{}.csv'.format(cust_id), '../dataset/Bank_Customer_Details.csv')
        date = df['Date'].values[-1:][0]
        cust_details = get_customer_details(df1, int(cust_id))
        offer = Offer(cust_details)
        season_scheme = offer.seasonal_offers(date)
        return season_scheme


if __name__ == "__main__":
    app.run(debug=True)