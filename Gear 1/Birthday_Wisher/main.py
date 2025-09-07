import datetime as dt
import pandas
import smtplib
import random
import os 


now = dt.datetime.now()
current_day = now.day
current_month = now.month

def send_email(message, to_email):
    email = "The email form where you want to send an email"
    word = "Your app password generated from your email(not the login password)"
    subject = "Subject: Happy Birthday!\n\n"
    full_msg = subject + message

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=word)
        connection.sendmail(from_addr=email, to_addrs=to_email, msg=full_msg.encode('utf-8'))

data = pandas.read_csv("birthdays.csv")

for (index, row) in data.iterrows():  
    if current_day == row["day"] and current_month == row["month"]:
        letter_file = f"letter_templates/letter_{random.randint(1, 5)}.txt"
        try:
            with open(letter_file, "r") as f:
                content = f.read()
                personalized_letter = content.replace("[NAME]", row["name"])
            send_email(personalized_letter, row["email"])
        except FileNotFoundError:
            print(f"Letter file {letter_file} not found.")
        except Exception as e:
            print(f"Failed to send email: {e}")
