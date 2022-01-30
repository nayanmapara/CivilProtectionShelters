import smtplib
from twilio.rest import Client
import os

email_sender_add= os.environ['email_sender_add']
email_password= os.environ['email_password']
account_sid = os.environ['account_sid']
auth_token = os.environ['auth_token']
message_sid = os.environ['message_sid']

def send_email(receiver_add,message):
    try:
        smtp_server=smtplib.SMTP("smtp.gmail.com",587)
        smtp_server.ehlo() #setting the ESMTP protocol
        smtp_server.starttls() #setting up to TLS connection
        smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()
        smtp_server.login(email_sender_add,email_password) #logging into out email id
        #sending the mail by specifying the from and to address and the message 
        smtp_server.sendmail(email_sender_add,receiver_add,message)
        smtp_server.quit()
        return True
    except Exception as e:
        print(e)
        return False

def send_message(text,numbers):
    client = Client(account_sid, auth_token) # setting up the twilio client
    message = client.messages.create(  
                              messaging_service_sid=message_sid, 
                              body=text,      
                              to=numbers 
                          )
    if message.sid == '':
        return True
    else:
        return False

def send_data(receiver_add,text,numbers):
    if send_email(receiver_add,text) and send_message(text,numbers) is True: # Checking if both the functions return True
        output = True
    else:
        output = False
    return output

def loc_info(address):
    # Code to be added here
    url = ''
    return url