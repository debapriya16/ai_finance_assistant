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
        pension = {
            "pension": [
                {
                    "scheme": "National Pension Plan",
                    "link": "https://www.moneyhelper.org.uk/en/pensions-and-retirement/pensions-basics/the-different-pensions-you-can-get-if-you-live-and-work-in-the-uk"
                }
            ]
        }
        return pension

    def healthcare_schemes(self):
        healthcare = {
            "healthcare": [
                {
                    "scheme": "Health insurance",
                    "link": "https://www.icicilombard.com/health-insurance/health-advantedge-insurance-for-family"
                }
            ]
        }
        return healthcare

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

    def student_scheme(self):
        student = {
            "student": [
                {
                    "scheme": "Student Bank Account",
                    "link": "https://www.natwest.com/current-accounts/student_account.html"
                },
                {
                    "scheme": "Student Laptop Offer",
                    "link" : "https://www.lenovo.com/in/en/d/students-offer"
                }
            ]
        }
        return student

    def restaurant_schemes(self):
        hotel = {
            "hotel": [
                {
                    "scheme": "Restaurant Offers",
                    "link": "https://www.tastecard.co.uk/dining-out"
                },
                {
                    "scheme": "CashBack Offers",
                    "link": "https://www.natwest.com/ukcashback1.html"
                },
                {
                    "scheme": "Recipe Videos",
                    "link": "https://www.youtube.com/watch?v=1HHfTZ9EpXw"
                }
            ]
        }
        return hotel

    def electoral_roll_schemes(self):
        elect = {
            "elect": [
                {
                    "scheme": "Voting Benefits",
                    "link": "https://www.derby.gov.uk/news/2022/march/voter-registration-benefits/"
                }
            ]
        }
        return elect

    def entertainment_scheme(self):
        entertain = {
            "entertain": [
                {
                    "scheme": "Movie Tickets",
                    "link": "https://in.bookmyshow.com/offers"
                },
                {
                    "scheme": "Gaming",
                    "link": "https://richardsonsfamilybowl.co.uk/offers/"
                }
            ]
        }
        return entertain


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
        elif age >= 20 and age <= 25:
            student = Products.student_scheme(self)
            return student

    def check_customer_preferences(self, df):
        x = get_investment_categories(df)
        y = x.nlargest(2)
        d = y.to_dict()
        scheme = {}
        for key in d:
            if key == "Travel":
                travel = Products.travel_offers(self)
                print(travel)
                scheme.update(travel)
            elif key == "Medical":
                med = Products.healthcare_schemes(self)
                scheme.update(med)
            elif key == "Restaurant":
                hotel = Products.restaurant_schemes(self)
                scheme.update(hotel)
            elif key == "Entertainment":
                entertain = Products.entertainment_scheme(self)
                scheme.update(entertain)
        return scheme

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

    def electoral_offers(self):
        e_roll = self.customer["Has_Electoral_Roll"].values[0]
        if e_roll == "No":
            elect = Products.electoral_roll_schemes(self)
            return elect
        else:
            return "No Voting Benefits found"



