
#objective: send a motivational quote via email on the current workday (change it to monday afterwards)
import datetime as dt
import pandas
import random
import smtplib
#use datetime module to get current day of week
now = dt.datetime.now()
weekday = now.weekday()
print(weekday)
MY_EMAIL = "testingpythondev@gmail.com"
MY_PASSWORD = "krcbnhefmircnqkn"


if weekday == 0:
#open the list of quotes in quotes.txt to get the list of quotes
    with open("quotes.txt") as quote_file:
        # creates a list of the quotes from lines in .txt file
        all_quotes = quote_file.readlines()
        # use the random module to choose a random quote
        random_quote = random.choice(all_quotes)
    print(random_quote)

    message_with_subject=(f"Subject:Motivation Monday!\n\n"
                          f"{random_quote}")
    #use smtplib to send the email to yourself
    #establish an SMTP connection
    with smtplib.SMTP("smtp.gmail.com") as connection:
        #start transport layer security
        connection.starttls()
        #login with the email address and the accompanying 'app password'
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="xecix12799@almaxen.com",
                            msg=message_with_subject
                            )
