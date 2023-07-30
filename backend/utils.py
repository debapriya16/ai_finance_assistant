"""
Utility file to retrieve Merchant Category from account transactions and
generate the appropriate finance prompt based on the customer interest.
Author: Debapriya Chakraborty
date: 28-07-2023
"""

import pandas as pd
from riskanalysis import RiskAnalysis


def read_datasets(path_acc, path_cust):
    n = 1000  # specify 'None' if want to read whole file
    df_acc = pd.read_csv(path_acc, delimiter=',', nrows=n)
    df_cust = pd.read_csv(path_cust, delimiter=',')
    nRow, nCol = df_acc.shape
    print(f'There are {nRow} rows and {nCol} columns')
    return df_acc, df_cust


def get_investment_categories(df_acc):
    inv_buckets = df_acc['Category'].value_counts()
    return inv_buckets


def get_customer_details(df, acc):
    cust_details = df.loc[df['Account_No'] == acc]
    return cust_details


class Products:
    """
    The product class which shows the lists of products a customer is eligible for
    """
    def __init__(self):
        pass

    def show_pension_schemes(self):
        name = "National Pension Plan"
        min = 50
        max = 5000
        pension = {
            "pension": [{"plan": name, "minimum_deposit": min, "maximum_deposit": max}]
        }
        return pension

    def show_mortgage_schemes(self):
        mortgage = {"plan": "Mortgage Scheme"}
        return mortgage

    def travel_offers(self):
        travel = {
            "travel": [
            {
                "scheme" : "travel insurance",
                "link": "https://www.natwest.com/insurance/travel-insurance.html"
            },
            {
                "scheme": "holiday loans",
                "link": "https://www.natwest.com/loans/holiday-loans-loans-for-a-holiday-natwest.html"
            },
            {
                "scheme": "travel cards",
                "link" : "https://www.natwest.com/credit-cards.html#find"
            }
            ]
        }
        return travel

    def risk_related_products(self):
        risk = {
            "credit_risk": [
                {
                    "scheme": "expert advisory",
                    "link": "https://www.fincart.com/financialplan.html"
                },
                {
                    "scheme": "Term Plans",
                    "link": "https://www.nidirect.gov.uk/articles/debt-management-plans"
                }
            ]
        }
        return risk

    def winter_season_products(self):
        season =  {
            "season" : [
                {
                    "scheme" : "Heating Boiler",
                    "link": "https://www.bosch-industrial.com/global/en/ocs/commercial-industrial/unimat-heating-boiler-ut-l-669463-p/"
                },
                {
                    "scheme": "Heaters",
                    "link": "https://www.nytimes.com/wirecutter/reviews/best-space-heaters/"
                },
                {
                    "scheme": "Power Saving Tips",
                    "link": "https://www.constellation.com/energy-101/energy-savings-tips/winter-energy-saving-tips.html"
                }
            ]
        }
        return season


class Offer:
    """
    Offer class for customers
    """
    def __init__(self, customer):
        self.customer = customer

    def check_age_offers(self):
        age = self.customer["Age"].values[0]
        if age >= 35:
            pension = Products.show_pension_schemes(self)
            return pension
        if age >= 20 and age <= 60:
            mortgage = Products.show_mortgage_schemes(self)
            return mortgage

    def check_customer_preferences(self):
        x = get_investment_categories(df)
        y = x.nlargest(2)
        d = y.to_dict()
        for key in d:
            if key == "Travel":
                travel = Products.travel_offers(self)
                print(travel)
                return travel

    def check_risk_analysis(self, account_id):
        ml = RiskAnalysis(account_id)
        risk_check = ml.model_results()
        if int(risk_check.iloc[0]) == 1:
            risk = Products.risk_related_products(self)
            return risk
        else:
            return "No Risk Detected"

    def seasonal_offers(self, date):
        month = date.split("-")[1]
        if int(month) >= 8:
            season = Products.winter_season_products(self)
            return season
        else:
            return "No Products suggested"






df, df1 = read_datasets('../dataset/account-statement.csv', '../dataset/Bank_Customer_Details.csv')
buckets = get_investment_categories(df)
print(buckets)
x = get_customer_details(df1, 4998365304)
offer = Offer(x)
print(offer.check_risk_analysis(4998365304))



