import requests
import smtplib
import os

JENKINS_URL = 'http://18.197.142.203:8080'

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

response = requests.get(JENKINS_URL)
if response.status_code == 200:
    print("App is healthy")
else:
    print('App is not healthy')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = "Subject: SITE DOWN!\nFix the issue!"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
