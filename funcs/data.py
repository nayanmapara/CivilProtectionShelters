from smtplib import SMTP
from twilio.rest import Client
from os import environ
from requests import get

# Getting Environment Variables
email_sender_add = environ['email_sender_add']
email_password = environ['email_password']
account_sid = environ['account_sid']
auth_token = environ['auth_token']
message_sid = environ['message_sid']
map_api_key = environ["azure_maps_api_key"]

def send_email(receiver_add,message):
    try:
        smtp_server = SMTP("smtp.gmail.com",587)
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
    # Getting JSON data from API
    json_data = get(f"https://atlas.microsoft.com/search/poi/json?api-version=1.0&query={address}&subscription-key={map_api_key}").json()
    lat, lon = json_data["results"][0]["position"].values() # Getting Lat and Long from JSON
    url = f"https://www.google.com/maps/place/{lat}+{lon}" # Making GoogleMaps URL of optained Lat and Long
    return url
