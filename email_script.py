from email.mime.text import MIMEText
from email.message import EmailMessage
import smtplib



def send_email(text):
    msg = EmailMessage()
    msg.set_content(MIMEText(text))
    msg['Subject'] = f'ERROR in Liceu PYTHON script'
    msg['From'] = "garretaserra+123@gmail.com"
    msg['To'] = "garretaserra@gmail.com"

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost:1025')
    s.send_message(msg)
    s.quit()

send_email('test')