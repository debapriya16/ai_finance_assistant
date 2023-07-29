import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score



class RiskAnalysis:
    def __init__(self, customer):
        self.customer = customer
        self.df = pd.read_csv('../dataset/Bank_Customer_Details.csv', delimiter=',')
    def convert_salary(self):
        self.df.loc[self.df["Estimated_Income"] == "40K - 60K", "Estimated_Income"] = random.randint(40000, 60000)
        self.df.loc[self.df["Estimated_Income"] == "60K - 80K", "Estimated_Income"] = random.randint(60000, 80000)
        self.df.loc[self.df["Estimated_Income"] == "80K - 120K", "Estimated_Income"] = random.randint(80000, 120000)
        self.df.loc[self.df["Estimated_Income"] == "Unknown", "Estimated_Income"] = random.randint(10000, 60000)
        self.df.loc[self.df["Estimated_Income"] == "120K +", "Estimated_Income"] = random.randint(120000, 140000)
        self.df.loc[self.df["Estimated_Income"] == "Less than 40K", "Estimated_Income"] = random.randint(20000, 40000)
        return self.df

    def create_dataset(self):
        self.df = self.convert_salary()
        self.df.loc[self.df['Credit_Score'] <= 500, 'Default'] = 1
        self.df.loc[self.df['Credit_Score'] > 500, 'Default'] = 0
        return self.df

    def feature_engineering(self):
        self.df = self.create_dataset()
        # Filling Null Values for Age
        self.df['Age'].fillna(int(self.df['Age'].mean()), inplace=True)
        self.df['No_Of_Months_On_Bank'].fillna(int(self.df['No_Of_Months_On_Bank'].mean()), inplace=True)
        self.df['Credit_Score'].fillna(int(self.df['Credit_Score'].mean()), inplace=True)
        self.df['Estimated_Income'].fillna(int(self.df['Estimated_Income'].mean()), inplace=True)
        self.df['Balance_Amount'].fillna(int(self.df['Balance_Amount'].mean()), inplace=True)
        self.df['Default'].fillna(int(self.df['Default'].mean()), inplace=True)
        # Dropping features which do not serve any purpose
        self.df.drop(columns=['Has_Credit_Card', 'Gender', 'EducationLevel', 'Marital_Status', 'Account_Type',
                         'No_Of_Linked_Accounts'], axis=1, inplace=True)
        # Dependent and Independent Variables
        self.X = self.df.iloc[:, :-1]  # Independent
        self.y = self.df.iloc[:, -1]  # Dependent

        # Train test split
        # split original DataFrame into two DataFrames
        self.X_test = self.X.iloc[:2500]
        self.X_train = self.X.iloc[2500:]

        self.y_test = self.y.iloc[:2500]
        self.y_train = self.y.iloc[2500:]

        self.index = np.where(self.X_test == 4998365304)[0][0]

        return self.X, self.y, self.X_test, self.y_test, self.X_train, self.y_train, self.index

    def find_feature_imp(self):
        # Feature Importance illustration using random forest
        forest_clf = RandomForestClassifier(n_estimators=100)
        forest_clf.fit(self.X, self.y)

        importances = forest_clf.feature_importances_
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(7, 7))
        plt.bar(range(len(indices)), importances[indices])
        plt.xticks(range(len(indices)), indices)
        plt.title("Feature importance")
        plt.xlabel('Index of a feature')
        plt.ylabel('importance')
        plt.show()

    def feature_scaling(self):
        # Feature Scaling
        self.X, self.y, self.X_test, self.y_test, self.X_train, self.y_train, self.index = self.feature_engineering()
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        self.X_train = sc.fit_transform(self.X_train)
        self.X_test = sc.transform(self.X_test)
        return self.X_train, self.X_test, self.y_test, self.y_train

    def model_results(self):
        self.X_train, self.X_test, self.y_test, self.y_train = self.feature_scaling()
        ##Model Selection with accu racy score and confusion matrix
        # Random Forest
        classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
        classifier.fit(self.X_train, self.y_train)
        y_pred_random = classifier.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred_random)
        print(cm)
        accuracy_score(self.y_test, y_pred_random)
        return pd.DataFrame(y_pred_random).iloc[self.index]


"""
# Using Naive Bayes
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
from sklearn.metrics import confusion_matrix, accuracy_score
y_pred_bayes = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred_bayes)
print(cm)
accuracy_score(y_test, y_pred_bayes)

# Using K Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier.fit(X_train, y_train)
y_pred_knearest = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred_knearest)
print(cm)
accuracy_score(y_test, y_pred_knearest)

# Using Decision Tree
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
classifier.fit(X_train, y_train)
y_pred_dtree = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred_dtree)
print(cm)
accuracy_score(y_test, y_pred_dtree)

# Support vector Classifier
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, y_train)
y_pred_svm = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred_svm)
print(cm)
accuracy_score(y_test, y_pred_svm)

"""
