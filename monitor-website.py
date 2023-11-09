import requests
import smtplib
import os
import paramiko
import time
import schedule

WEBSITE_URL = os.environ.get('WEBSITE_URL')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_email_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: SITE DOWN!\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

def restart_container():
    print('Restarting application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='remote-server-addr', username='ubuntu', key_filename='/home/an3a/.ssh/admin-ssh-key.pem')
    stdin, stdout, stderr = ssh.exec_command('docker start 432832hiidh')
    print(stdout.readlines())
    ssh.close()

def restart_server():
    print('Restarting server...')
    # TODO

def monitor_application():
    try:
        response = requests.get(WEBSITE_URL)
        if response.status_code == 200:
            print("App is healthy")
        else:
            print(f'App is not healthy! Status code: {response.status_code}')
            msg = f"Subject: SITE DOWN!\n App returned status code {response.status_code}"
            send_email_notification(msg)
            restart_container()

    except Exception as ex:
        print(f'Connection error happened')
        msg = "Subject: SITE DOWN!\n App not accessible"
        send_email_notification(msg)

        print('Rebooting the server')

        restart_server()

        # TODO - wait until server is up again
        time.sleep(5)
        restart_container()

schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()