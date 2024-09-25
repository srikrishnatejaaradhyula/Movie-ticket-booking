import  smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os


def send_email(sender,receiver,subject,body,attachment=None):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body)) 
    if attachment:
        filename = attachment
        path = os.path.join(os.getcwd(), filename)
        with open(path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="csv")
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(attachment)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 
    smtp_username = sender
    smtp_password = 'fwxwdukdgyjbvaex'

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, message.as_string())

def send_email_html(sender,receiver,subject,body,attachment=None):
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "html")) 
    if attachment:
        filename = attachment
        path = os.path.join(os.getcwd(), filename)
        with open(path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="csv")
            attachment.add_header("Content-Disposition", "attachment", filename=filename)
            message.attach(attachment)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587 
    smtp_username = sender
    smtp_password = 'fwxwdukdgyjbvaex'

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, message.as_string())