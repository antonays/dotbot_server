from flask_mail import Mail, Message
from app import mail

def send_email(address, subject, contents):

    msg = Message(subject,
                  sender="dotbot@dotbot.com",
                  recipients=[address])
    msg.body = "asjdnaksd"

    mail.send(msg)