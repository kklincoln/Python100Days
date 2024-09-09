# import smtplib
#
# my_email = "testingpythondev@gmail.com"
# my_password = "krcbnhefmircnqkn"
#
# #establish SMTP server connection
# with smtplib.SMTP("smtp.gmail.com") as connection:
#     #start transport layer security to secure the connection to email server; (encrypts messages)
#     connection.starttls()
#     connection.login(user=my_email,password=my_password)
#     connection.sendmail(from_addr=my_email,
#                         to_addrs="xecix12799@almaxen.com",
#                         msg="Subject:Hello\n\nThis is the body of my email"
#                         )
#
# #working with Datetime Module

# import datetime as dt
# now =  dt.datetime.now() #datetime type
# year = now.year #int type
# month = now.month
# day_of_week = now.day
# print(year)

# date_of_birth = dt.datetime(year=,month=,day=,hour=)


