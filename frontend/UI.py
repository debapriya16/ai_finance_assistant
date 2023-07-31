from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
import panel as pn
pn.extension('tabulator')
import numpy as np
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import webbrowser
from datetime import date
import customtkinter
import requests
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set the appearance
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Choose customer
customer_id = '1'

if customer_id == '1':
    cust = '4'
elif customer_id == '2':
    cust = '41'

# Create the root
root = customtkinter.CTk()
root.geometry("1500x1000")

# Read in the transaction categories data
test_data_trans = requests.get('http://127.0.0.1:5000/transaction/amount/' + customer_id)
trans_json = test_data_trans.json()
categories_data = pd.DataFrame.from_dict(trans_json, orient="index")

# Read in the transaction categories data
test_data_trans_no = requests.get('http://127.0.0.1:5000/transaction/categories/'+ customer_id)
trans_json_no = test_data_trans.json()
categories_no_data = pd.DataFrame.from_dict(trans_json, orient='index')

# Read in the customer data
test_data_cust = requests.get('http://127.0.0.1:5000/customer/'+ customer_id)
cust_json = test_data_cust.json()
cust_data = pd.DataFrame.from_dict(cust_json, orient="index")

# Read in the offer data
test_data_offer = requests.get('http://127.0.0.1:5000/offers/'+ customer_id)
json_offer = test_data_offer.json()
offer_data = pd.json_normalize(json_offer)

# Read in the seasonal offer data
test_data_season = requests.get('http://127.0.0.1:5000/offers/seasonal/'+ customer_id)
json_season = test_data_season.json()
season_data = pd.json_normalize(json_offer)


# Adds the title bar
title_frame = customtkinter.CTkFrame(root, width=5000, height=100, fg_color='#421462')
title_frame.place(x=0, y=0)

# Insert NW logo
finance_img = Image.open('/Users/imogensole/Desktop/Hackathon/nwg-social-media-logo.png')
resized_img = finance_img.resize((70,100))
img = ImageTk.PhotoImage(resized_img)
title_frame.label = Label(title_frame, image = img)
title_frame.label.pack(side=LEFT)

# Add the title
title = customtkinter.CTkLabel(title_frame,
                               text="  Financial Assistant",
                               font=('Interstate Regular', 40),
                               width=1500,
                               anchor="w")
title.pack(side=RIGHT)

# Add tips sidebar
sidebar = customtkinter.CTkFrame(root, width=600,
                                    height=900,
                                    fg_color='#421462',
                                    corner_radius=0,
                                    border_color='#421462',
                                    border_width=3)
sidebar.place(x=0, y=200)

tips_title_frame = customtkinter.CTkFrame(root, width=302,
                                    height=1000,
                                    fg_color='#421462',
                                    corner_radius=0,
                                    border_color='#421462',
                                    border_width=3)
tips_title_frame.place(x=0, y=100)

tips_frame = customtkinter.CTkFrame(root, width=402,
                                    height=900,
                                    fg_color='#421462',
                                    corner_radius=0,
                                    border_color='#421462',
                                    border_width=3)
tips_frame.place(x=0, y=200)



tips_title = customtkinter.CTkLabel(tips_title_frame,
                               text="  Top Tips for You",
                               font=('Interstate Regular', 30),
                               width=100,
                               anchor="nw")
tips_title.place(rely=0.03, anchor="nw")


# Get offers from json
offers = json_offer.keys()

# travel offer
# Detects whether customer has travel offer
if 'travel' in offers:
    travel_title = customtkinter.CTkLabel(tips_frame,
                                        text="  Travel:",
                                        font=('Interstate Regular', 20, 'bold'),
                                        width=285,
                                        anchor="nw",
                                        bg_color='#8982b4')
    travel_title.pack(anchor=W)
    #Creates the tip
    global travel_tip
    travel_tip = 'We noticed you recently made a travel purchase. Find some useful offers below.'
    tips = Message(tips_frame,
                   text=travel_tip,
                   width=295,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W, ipady=5)

    # Extracts the offer links
    travel_links = json_offer['travel']

    # Iterates over each link
    for n in range(len(travel_links)):
        link = travel_links[n]

        # Creates the link
        travel_link = Message(tips_frame, text=link['scheme'],
                            cursor='hand2',
                            font=('San Francisco', 15, 'underline'),
                            width=295,
                            bg='#421462',
                            fg='white')
        travel_link.bind('<Button-1>', lambda x: webbrowser.open_new(link['link']))
        travel_link.pack(anchor=W)

else:
    pass

# creates the eating out tip

eating_out_spend = trans_json["Restaurant"]

if eating_out_spend > 100:
    eo_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Eating Out:                                     ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                          bg_color='#8982b4')
    eo_title.pack(anchor=W)
    global eo_tip
    eo_tip = 'This month you spent £' + format(float(eating_out_spend), '.2f') + ' eating out. Here are some fun recipes you could try at home to save money.'
    tips = Message(tips_frame,
                   text=eo_tip,
                   width=290,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    eat_link = Message(tips_frame,
                       text='Check out these recipes!',
                       cursor='hand2',
                       font=('San Francisco', 15, 'underline'),
                       width=295,
                       bg='#421462',
                       fg='white')
    eat_link.bind('<Button-1>', lambda x:webbrowser.open_new("https://www.bbcgoodfood.com/recipes/collection/cheap-eat-recipes"))
    eat_link.pack(anchor=W)

else:
    pass

# Creates a pension tip
if 'pension' in offers:
    pension_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Pension:                     ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                          bg_color='#8982b4')
    pension_title.pack(anchor=W)
    pension = json_offer['pension']
    global pension_tip
    pension_tip = ('Have you thought about a pension plan?')
    tips = Message(tips_frame,
                   text=pension_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    eat_link = Message(tips_frame,
                       text=json_offer['pension'][0]["scheme"],
                       cursor='hand2',
                       font=('San Francisco', 15, 'underline'),
                       width=295,
                       bg='#421462',
                       fg='white')
    eat_link.bind('<Button-1>',
                  lambda x: webbrowser.open_new(json_offer['pension'][0]["link"]))
    eat_link.pack(anchor=W)
else:
    pass

# Electoral Register
if 'elect' in offers:
    elect_title = customtkinter.CTkLabel(tips_frame,
                                          text="  The Electoral Register:            ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                         bg_color='#8982b4')
    elect_title.pack(anchor=W)
    elect = json_offer['elect']
    global elect_tip
    elect_tip = ('Are you on the electoral roll? Joining the electoral roll could benefit your financial health. For more information on the benefits see below.')
    tips = Message(tips_frame,
                   text=elect_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    elect_link = Message(tips_frame,
                       text=json_offer['elect'][0]["scheme"],
                       cursor='hand2',
                       font=('Interstate Regular', 15, 'underline'),
                       width=295,
                       bg='#421462',
                       fg='white')
    elect_link.bind('<Button-1>',
                  lambda x: webbrowser.open_new(json_offer['elect'][0]["link"]))
    elect_link.pack(anchor=W)

else:
    pass

# healthcare Register
if 'healthcare' in offers:
    healthcare_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Healthcare:            ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                         bg_color='#8982b4')
    healthcare_title.pack(anchor=W)
    healthcare = json_offer['healthcare']
    healthcare_tip = ('Have you got healthcare? For more information see here:')
    tips = Message(tips_frame,
                   text=healthcare_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    healthcare_link = Message(tips_frame,
                       text=json_offer['healthcare'][0]["scheme"],
                       cursor='hand2',
                       font=('Interstate Regular', 15, 'underline'),
                       width=295,
                       bg='#421462',
                       fg='white')
    healthcare_link.bind('<Button-1>',
                  lambda x: webbrowser.open_new(json_offer['healthcare'][0]["link"]))
    healthcare_link.pack(anchor=W)

else:
    pass

# Creates an entertainment tip
if 'entertain' in offers:
    entertain_amnt = trans_json['Entertainment']
    entertain_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Entertainment:                        ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                        bg_color='#8982b4')
    entertain_title.pack(anchor=W)
    entertain = json_offer['entertain']
    entertain_tip = ('We noticed you spent £' + str(entertain_amnt) + ' on entertainment this month. Here are some great offers that might interest you!')
    tips = Message(tips_frame,
                   text=entertain_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    entertain_links = json_offer['entertain']

    for n in range(len(entertain_links)):
        link = entertain_links[n]

        # Creates the link
        entertain_link = Message(tips_frame, text=link['scheme'],
                            cursor='hand2',
                            font=('San Francisco', 15, 'underline'),
                            width=295,
                            bg='#421462',
                            fg='white')
        entertain_link.bind('<Button-1>', lambda x: webbrowser.open_new(link['link']))
        entertain_link.pack(anchor=W)

else:
    pass

# Creates a hotel tip
if 'hotel' in offers:
    hotel_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Hotel:                              ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                         bg_color='#8982b4')
    hotel_title.pack(anchor=W)
    hotel = json_offer['hotel']
    hotel_tip = ('Here are some great hotel offers we think might interest you:')
    tips = Message(tips_frame,
                   text=hotel_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    hotel_links = json_offer['hotel']

    for n in range(len(hotel_links)):
        link = hotel_links[n]

        # Creates the link
        hotel_link = Message(tips_frame, text=link['scheme'],
                            cursor='hand2',
                            font=('San Francisco', 15, 'underline'),
                            width=295,
                            bg='#421462',
                            fg='white')
        hotel_link.bind('<Button-1>', lambda x: webbrowser.open_new(link['link']))
        hotel_link.pack(anchor=W)
else:
    pass

# Creates a student tip
if 'student' in offers:
    student_title = customtkinter.CTkLabel(tips_frame,
                                          text="  Students:    ",
                                          font=('Interstate Regular', 20, 'bold'),
                                          width=285,
                                          anchor="nw",
                                           bg_color='#8982b4')
    student_title.pack(anchor=W)
    student = json_offer['student']
    student_tip = ('Are you a student? There are some great opportunites and offers available for students - including the natwest student account.')
    tips = Message(tips_frame,
                   text=student_tip,
                   width=295,
                   anchor=W,
                   bg='#421462',
                   fg='white')
    tips.pack(anchor=W)

    student_links = json_offer['student']

    for n in range(len(student_links)):
        link = student_links[n]

        # Creates the link
        student_link = Message(tips_frame, text=link['scheme'],
                            cursor='hand2',
                            font=('San Francisco', 15, 'underline'),
                            width=295,
                            bg='#421462',
                            fg='white')
        student_link.bind('<Button-1>', lambda x: webbrowser.open_new(link['link']))
        student_link.pack(anchor=W)
else:
    pass

# create savings goal frame
spend_frame = customtkinter.CTkFrame(root, width=600,
                                    height=400,
                                    fg_color='#8982b4',
                                    corner_radius=0)
spend_frame.pack_propagate(False)
spend_frame.place(x=302, y=100)

# Spending breakdown frame
save_frame_1 = customtkinter.CTkFrame(root, width=600,
                                    height=400,
                                    fg_color='#8982b4',
                                    border_width=0,
                                    corner_radius=0)
save_frame_1.pack_propagate(False)
save_frame_1.place(x=902, y=100)

save_frame = customtkinter.CTkFrame(root, width=600,
                                    height=400,
                                    fg_color='#8982b4',
                                    border_width=0,
                                    corner_radius=0)
save_frame.pack_propagate(False)
save_frame.place(x=902, y=200)

#Monthly spending pie chart

colours = ["#A58CC3", "#C8B9D7", "#F4F0E8"]

keys = trans_json.keys()
labels = ["other"]
pie_amount = [0]

total_spend = 0

for key in keys:
    total_spend += trans_json[key]


for key in keys:
    if trans_json[key] == 0:
        pass
    elif (trans_json[key]/total_spend)*100 > 5:
        pie_amount.append(trans_json[key])
        labels.append(key)
    else:
        pie_amount[0] += trans_json[key]

fig = plt.figure(figsize=(1.8,1.8), facecolor='#8982b4')

plt.pie(pie_amount,
        autopct='%1.1f%%',
        colors=colours,
        labels=labels,
        textprops={'fontsize': 4},
        pctdistance=0.5,
        labeldistance=1.3)


canvas = FigureCanvasTkAgg(fig, master=spend_frame)
canvas.draw()
canvas.get_tk_widget().place(relx=0.03, rely=0.1, height=350, width=550)

# Spending section title

spend_title_frame = customtkinter.CTkFrame(root, width=302,
                                    height=100,
                                    fg_color='#8982b4',
                                    corner_radius=0,
                                    border_color='#8982b4',
                                    border_width=3)
spend_title_frame.place(x=320, y=120)

spend_title = customtkinter.CTkLabel(spend_title_frame,
                            text="  Your Spending this Month",
                            font=('Interstate Regular', 30),
                            width=570,
                            anchor="w",
                            bg_color='#421462',
                            text_color="white")
spend_title.pack(side=TOP, ipady=5)


# Savings Planner

save_title_frame = customtkinter.CTkFrame(root, width=302,
                                    height=100,
                                    fg_color='#421462',
                                    corner_radius=100,
                                    border_width=3)
save_title_frame.place(x=920, y=120)

save_title = customtkinter.CTkLabel(save_title_frame,
                            text="  Your Savings Goals",
                            font=('Interstate Regular', 30),
                            width=565,
                            anchor="w",
                            bg_color='#421462',
                            text_color="white")
save_title.pack(side=TOP, ipady=5)

# Creating an Entry widget

save_space = customtkinter.CTkLabel(save_frame,
                               text="  ",
                               font=('Interstate Regular', 30),
                               width=500,
                               height=70,
                               anchor="w",
                                text_color='#421462')
save_space.pack(side=TOP)

# Calculate current amount
savings = np.round(cust_json["Balance_Amount"][cust], decimals=2)

balance_frame = customtkinter.CTkFrame(root, width=500,
                                    height=85,
                                    fg_color='#421462',
                                    bg_color='#8982b4',
                                    border_width=0,
                                    corner_radius=30)
balance_frame.pack_propagate(False)
balance_frame.place(x=950, y=180)

balance_title = customtkinter.CTkLabel(balance_frame,
                            text="  You currently have £" + str(savings) + ' in savings.',
                            font=('Interstate Regular', 20),
                            width=200,
                            anchor="w",
                            bg_color='#421462',
                            text_color="white")
balance_title.place(x=50, y=15)



# Allows user to input savings goal
save_goal = customtkinter.CTkEntry(save_frame, placeholder_text="Enter your savings goal", width=500)
save_goal.pack()

# Allows user to input goal date
date_goal = customtkinter.CTkEntry(save_frame, placeholder_text="Goal Date (dd-mm-yyyy)", width=500)
date_goal.pack()



#Calculates savings plan

def month_save(goal, date):
    today = datetime.today()

    months = (date.year - today.year) * 12 + (date.month - today.month)

    monthly_save = (float(goal) - savings) / float(months)
    return(monthly_save)


def calc_savings():
    global goal
    goal = save_goal.get()
    date = datetime.strptime(date_goal.get(), '%d-%m-%Y')

    percent_of_goal = round(float(total_savings) / float(goal) *100, 2)

    save_per_month = month_save(goal, date)

    space = customtkinter.CTkLabel(save_frame,
                                   text="",
                                   bg_color='#8982b4')
    space.pack()

    label = customtkinter.CTkLabel(save_frame, text = "You need to save £" + str(save_per_month) + " per month to meet your goal",
                                   bg_color='#8982b4',
                                   font=('Interstate Regular', 18),
                                   text_color='#421462')
    label.pack()

    progress = customtkinter.CTkLabel(save_frame, text = "You are " + str(percent_of_goal) + f"% of the way to reaching your savings goal!",
                                      bg_color='#8982b4',
                                      font=('Interstate Regular', 18),
                                      text_color='#421462')
    progress.pack()

    space2 = customtkinter.CTkLabel(save_frame,
                                   text="",
                                   bg_color='#8982b4')
    space2.pack()

    progressbar = customtkinter.CTkProgressBar(save_frame,
                                               orientation="horizontal",
                                               progress_color="#421462",
                                               width=200,
                                               height=30)
    progressbar.set((percent_of_goal / 100))
    progressbar.pack()


#Calculate button

save_button = customtkinter.CTkButton(save_frame, text = "Calculate Savings Plan",
                                      command=calc_savings,
                                      fg_color="#421462",
                                      anchor="center",
                                      width=500)
save_button.pack()

#Financial health
health_frame = customtkinter.CTkFrame(root, width=600,
                                    height=500,
                                    fg_color='#8982b4',
                                    border_width=0,
                                    corner_radius=0)
health_frame.pack_propagate(False)
health_frame.place(x=302, y=500)

health_title = customtkinter.CTkLabel(health_frame,
                            text="  Your Financial Health",
                            font=('Interstate Regular', 30),
                            width=570,
                            anchor="w",
                            bg_color='#421462',
                            text_color="white")
health_title.pack(side=TOP, ipady=5)

cred_space = Message(health_frame,
                   text="      ",
                   width=100000,
                   bg='#8982b4',
                   fg='white',
                   font=('Interstate Regular', 20),
                    padx=200)

cred_space.pack()

cred_score = cust_json['Credit_Score'][cust]

credit_score = Message(health_frame,
                   text="Your credit score is:  " + str(cred_score),
                   width=600,
                   bg='#421462',
                   fg='white',
                   font=('Interstate Regular', 20))

credit_score.pack()

# Credit Risk

if 'credit_risk' in offers:
    credit_title = customtkinter.CTkLabel(health_frame,
                                        text="  Credit Risk:",
                                        font=('Interstate Regular', 20, 'bold'),
                                        width=300,
                                        anchor="nw")
    credit_title.pack(anchor=W)
    #Creates the tip
    credit_tip = 'For more information about credit risk:'
    tips = Message(health_frame,
                   text=credit_tip,
                   width=500,
                   fg='#421462',
                   bg='#8982b4',
                   font = ('Interstate Regular', 18))
    tips.pack(anchor=W, ipady=5)

    # Extracts the offer links
    credit_links = json_offer['credit_risk']

    # Iterates over each link
    for n in range(len(credit_links)):
        link = credit_links[n]

        # Creates the link
        credit_link = Message(health_frame, text=link['scheme'],
                            cursor='hand2',
                            font=('Interstate Regular', 18, 'underline'),
                            width=400,
                            bg='#8982b4',
                            fg='#421462')
        credit_link.bind('<Button-1>', lambda x: webbrowser.open_new(link['link']))
        credit_link.pack()

    credit_space = customtkinter.CTkLabel(tips_frame,
                                               text="     ",
                                               width=300,
                                               anchor="nw")
    credit_space.pack(anchor=W)
else:
    pass

# Seasonal
seasonal_frame = customtkinter.CTkFrame(root, width=600,
                                    height=500,
                                    fg_color='#8982b4',
                                    border_width=0,
                                    corner_radius=0)
seasonal_frame.pack_propagate(False)
seasonal_frame.place(x=902, y=500)

seasonal_title = customtkinter.CTkLabel(seasonal_frame,
                            text="  Seasonal Offers",
                            font=('Interstate Regular', 30),
                            width=570,
                            anchor="w",
                            bg_color='#421462',
                            text_color="white",
                            corner_radius=200)
seasonal_title.pack(side=TOP, ipady=5)

today = date(2023, 12, 12)

date_display = customtkinter.CTkLabel(seasonal_frame,
                            text= '    Today\'s Date:  ' + str(today),
                            font=('Interstate Regular', 25),
                            width=570,
                            anchor="w",
                            text_color='#421462',
                            corner_radius=200)
date_display.pack(side=TOP, ipady=5)

if today.month in [12, 1, 2]:
    winter_tip = 'As the weather gets colder, manage your heating expenses with the offers below.'
    tips = Message(seasonal_frame,
                   text=winter_tip,
                   width=520,
                   bg='#8982b4',
                   fg='#421462',
                   anchor=W,
                   font=('Interstate Regular', 18))
    tips.pack(ipady=10)
elif today.month in [3, 4, 5]:
    season = 'spring'
elif today.month in [6, 7, 8]:
    season = 'summer'
else:
    season = 'autumn'

seasonal_offers = json_season["season"]

for n in range(len(seasonal_offers)):
    offer = seasonal_offers[n]
    link = offer["link"]
    label = offer["scheme"]
    # Creates the link
    offer_link = Message(seasonal_frame, text=label,
                          cursor='top_right_corner',
                          font=('Interstate Regular', 18, 'underline'),
                          width=600,
                          bg='#8982b4',
                          fg='#421462')
    offer_link.bind('<Button-1>', lambda x: webbrowser.open_new(link))
    offer_link.pack()

account_no = customtkinter.CTkLabel(root,
                                    text = "Account Number:  " + str(cust_json["Account_No"][cust]),
                                    font=('Interstate Regular', 20),
                                    bg_color='#421462',
                                    text_color='#8982b4')

account_no.place(x=1200, y=60)


root.mainloop()



