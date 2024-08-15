#Gmail(smtp.gmail.com), Yahoo(smtp.mail.yahoo.com), Hotmail(smtp.live.com), Outlook(smtp-mail.outlook.com)
import datetime as dt
import pandas
import random
import smtplib

MY_EMAIL = "testingpythondev@gmail.com"
MY_PASSWORD = ""
today = dt.datetime.now()
today_touple = (today.month, today.day)
data = pandas.read_csv("birthdays.csv")

#create a cictionary from the values iterated through in the csv file
birthday_dict = {(data_row["month"],data_row["day"]): data_row for (index, data_row) in data.iterrows()}

#check if the today_touple matches any of the keys within the dictionary created
print(birthday_dict[today_touple])
if today_touple in birthday_dict:
    bday_person = birthday_dict[today_touple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

    #open the file of the randomly selected letter and replace the name with the name of the bday person
    with open(file_path) as letter_file:
        contents = letter_file.read()
        bday_letter = contents.replace("[NAME]",bday_person["name"])
        bday_name = bday_person["name"]

    #establish a SMTP commection and enable transport layer security(encryption)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=bday_person["email"],
                            msg=f"Subject:Happy Birthday {bday_name}!\n\n{bday_letter}"
                            )
