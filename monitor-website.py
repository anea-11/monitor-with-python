import requests
import smtplib
import os

JENKINS_URL = 'http://18.197.142.203:8080'

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_email_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: SITE DOWN!\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

try:
    response = requests.get(JENKINS_URL)
    if response.status_code == 200:
        print("App is healthy")
    else:
        print(f'App is not healthy! Status code: {response.status_code}')
        msg = f"Subject: SITE DOWN!\n App returned status code {response.status_code}"
        send_email_notification(msg)

except Exception as ex:
    print(f'Connection error happened')
    msg = "Subject: SITE DOWN!\n App not accessible"
    send_email_notification(msg)