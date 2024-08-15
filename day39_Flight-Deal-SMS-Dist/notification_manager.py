import os
from twilio.rest import Client
import smtplib
from dotenv import load_dotenv

load_dotenv(f"{os.getcwd()}/.env")

TWILIO_API_KEY = os.environ.get("TWILIO_API_KEY")

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
        self.twilio_number = os.environ.get("TWILIO_NUMBER")
        self.twilio_recipient = os.environ.get("RECIPIENT_NUMBER")
        self.smtp_sender_email = os.environ.get("SMTP_SENDER_EMAIL")
        self.smtp_sender_password = os.environ.get("SMTP_PASSWORD")
        self.connection = smtplib.SMTP(os.environ.get["SMTP_ADDRESS"])



    def send_sms(self,message_body):
        message = self.client.messages.create(
            body=message_body,
            from_=self.twilio_number,
            to=self.twilio_recipient
    )
        #print if successful
        print(message.sid)


    def send_emails(self, email_list, email_body):
        # establish SMTP commection and enable transport layer security(encryption)
        with self.connection:
            self.connection.starttls()
            self.connection.login(user=self.smtp_sender_email, password=self.smtp_sender_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.smtp_sender_email,
                    to_addrs=email,
                    msg=f"Subject: ALERT: New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )