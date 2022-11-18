import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from get_weather import run


def send(email, pw):
    from_address = "david.baussart@gmail.com"
    to_address = "david.baussart@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Your daily weather forecast ❤️"
    msg['From'] = "david.baussart@gmail.com"
    msg['To'] = "david.baussart@gmail.com"

    # Create the message (HTML).
    html = run()

    # Record the MIME type - text/html.
    part1 = MIMEText(html, 'html')

    # Attach parts into message container
    msg.attach(part1)

    # Credentials
    username = email
    password = pw

    # Sending the email
    ## note - this smtp config worked for me, I found it googling around, you may have to tweak the # (587) to get yours to work
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(from_address, to_address, msg.as_string())  
    server.quit()

email = sys.argv[1]
pw = sys.argv[2]

send(email, pw)
