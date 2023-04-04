import threading
import requests
from ..config.config import Configuration


def send_email(to, subject, msg):
    headers = {
        "user-agent": "Application", "Accept": "*/*",
        "Content-Type": "application/json; charset=utf-8"
    }
    body = {
        "toEmail": to,
        "toCc": "",
        "subject": subject,
        "msg": msg
    }
    response = requests.post(url=Configuration.get_Property("mail_api"), headers=headers, json=body)
    print("response email :: " + response.text)


def send_mail_in_thread(to, subject, msg):
    thread = threading.Thread(target=send_email, args=(to, subject, msg))
    thread.start()


email_api_msg91_headers = {'Content-Type': "application/JSON",
                           'Accept': "application/json", 'authkey': "375106ATCatDUwIZ26305eba8P1"}


def send_email_msg91_payload(to, template_id, variable1, variable2, variable3):
    payload = {
        "to": [
            {
                "name": "",
                "email": to
            }
        ],
        "from": {
            "name": "SabPaisa",
            "email": "noreply@mail.sabpaisa.in"
        },
        "cc": [],
        "bcc": [],
        "domain": "mail.sabpaisa.in",
        "mail_type_id": "3",
        "template_id": template_id,
        "variables": {
            "VAR1": variable1,
            "VAR2": variable2,
            "VAR3": variable3
        }
    }
    return payload


def send_plan_subscribed_msg91_payload(to, template_id, variable1, variable2, variable3, variable4, variable5,
                                       variable6):
    payload = {
        "to": [
            {
                "name": "",
                "email": to
            }
        ],
        "from": {
            "name": "SabPaisa",
            "email": "noreply@mail.sabpaisa.in"
        },
        "cc": [{"email": "mk274474@gmail.com"}],
        "bcc": [],
        "domain": "mail.sabpaisa.in",
        "mail_type_id": "3",
        "template_id": template_id,
        "variables": {
            "VAR1": variable1,
            "VAR2": variable2,
            "VAR3": variable3,
            "VAR4": variable4,
            "VAR5": variable5,
            "VAR6": variable6
        }
    }
    return payload
