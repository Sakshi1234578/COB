from api.config.config import Configuration
from ..utils import emails
from ..utils.emails import send_mail_in_thread
import traceback
import requests
import json

email_url_msg19 = Configuration.get_Property("EMAIL_API_MSG91")
email_url = Configuration.get_Property("EMAIL_VERIFICATION_URL")
msg91_headers = emails.email_api_msg91_headers


def validate_email(to, name, user_name, msg):
    try:
        payload_data = emails.send_email_msg91_payload(to, "mail-verification", name, user_name, msg)
        mail_response = requests.post(email_url_msg19, data=json.dumps(payload_data), headers=msg91_headers)
        response_mail_data = mail_response.json().get("data")
        print("email response data :", response_mail_data)
        print("email send at ", to)
        if response_mail_data is None:
            message = f"Hello {name}, Here is your link {msg}"
            send_mail_in_thread(to, "verification link for cob sabpaisa", message)
            print("sending mail using msg91")
    except Exception:
        traceback.print_exc()


def validate_otp_email(to, otp_for, name, otp):
    try:
        payload_data = emails.send_email_msg91_payload(to, "otp-request", otp_for, name, otp)
        mail_response = requests.post(email_url_msg19, data=json.dumps(payload_data), headers=msg91_headers)
        response_mail_data = mail_response.json().get("data")
        print("email response data :", response_mail_data)
        print("email send at ", to)
        if response_mail_data is None:
            message = f"Your OTP is {otp}, for {otp_for}"
            headers = f"OTP for {otp_for}"
            send_mail_in_thread(to, headers, message)
            print("sending mail using msg91")
    except Exception:
        traceback.print_exc()


def validate_subscribed_and_plan_email(to, name, url):
    try:
        payload_data = emails.send_email_msg91_payload(to, "cob-subscribed-plan", "SabPaisa", name, url)
        mail_response = requests.post(email_url_msg19, data=json.dumps(payload_data), headers=msg91_headers)
        response_mail_data = mail_response.json().get("data")
        print("email response data :", response_mail_data)
        print("email send at ", to)
        if response_mail_data is None:
            message = f"Thank you for choosing SabPaisa for all your payment needs! " \
                      f"Our team will get in touch with you for the next steps. " \
                      f"In case you have not filled up your KYC form, please click here", {url}
            send_mail_in_thread(to, "Your Product Subscription with SabPaisa", message)
            print("sending mail using msg91")
    except Exception:
        traceback.print_exc()


def validate_subscribed_and_plan_internal_mail(to, template_name, var1, var2, var3, var4, var5, var6):
    try:
        payload_data = emails.send_plan_subscribed_msg91_payload(to, template_name, var1, var2, var3, var4,
                                                                 var5, var6)
        mail_response = requests.post(email_url_msg19, data=json.dumps(payload_data), headers=msg91_headers)
        response_mail_data = mail_response.json().get("data")
        print("email response data :", response_mail_data)
        print("email send at ", to)
    except Exception:
        traceback.print_exc()
