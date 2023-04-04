import threading
import time
from ..utils import emails
from ..databaseModels.OTP import OTP
from api.utils import generator
from api.enums.otpcodes import OtpStatus, OtpType, OtpFor
from ..config.config import Configuration
from ..databaseModels.login_master import login_master
from ..utils import Sms
from ..DatabaseService import email_service


def save_otp(otp):
    contactDetail = None
    if not otp.get("email") and not otp.get("mobile_number"):
        return {"status": False, "message": "Please provide email or mobile number"}
    if (
            otp.get("otp_for").lower() == OtpFor.UPDATE_PASSWORD.value.lower()
            or otp.get("otp_for").lower() == OtpFor.FORGOT_PASSWORD.value.lower()
    ):
        contactDetail = get_mobile_number(otp.get("email"))
        if contactDetail == "Email is not correct":
            return "Email is not correct"
    otp = OTP(**otp)
    otp.otp = generator.generate_otp()
    otp.status = OtpStatus.PENDING.value
    otp.verification_token = generator.generate_verification_token()
    if contactDetail:
        name = login_master.objects.get(email=otp.email).name
        send_otp_sms(contactDetail, "Your OTP is {} for {}".format(otp.otp, otp.otp_for))
        email_service.validate_otp_email(otp.email, otp.otp_for, name, otp.otp)
    elif otp.otp_type.lower() == OtpType.BOTH.value.lower():
        if not otp.email or not otp.mobile_number:
            return {
                "status": False,
                "message": "Please provide both email and mobile number",
            }
        else:
            name = login_master.objects.get(email=otp.email).name
            send_otp_sms(contactDetail, "Your OTP is {} for {}".format(otp.otp, otp.otp_for))
            email_service.validate_otp_email(otp.email, otp.otp_for, name, otp.otp)
    elif otp.otp_type.lower() == OtpType.PHONE.value.lower():
        otp.otp_type = OtpType.PHONE.value
        send_otp_sms(otp.mobile_number, "Your OTP is {} for {}".format(otp.otp, otp.otp_for))
    elif otp.otp_type.lower() == OtpType.EMAIL.value.lower():
        otp.otp_type = OtpType.EMAIL.value
        name = login_master.objects.get(email=otp.email).name
        email_service.validate_otp_email(otp.email, otp.otp_for, name, otp.otp)
    else:
        return {"status": False, "message": "Invalid OTP type. Valid types are: Phone, Email"}
    otp.save()
    expire_otp_thread(otp.id)
    return {"status": True, "verification_token": otp.verification_token}


def expire_otp(otp_id: int):
    otp = OTP.objects.get(id=otp_id)
    if otp.status == OtpStatus.PENDING.value:
        otp.is_expired = True
        otp.status = OtpStatus.EXPIRED.value
        otp.save()
    return {"status": True}


def expire_otp_thread(otp_id: int):
    otp_expire_time = Configuration.get_Property("OTP_EXPIRE_TIME")

    class expire_otp_inner_thread(threading.Thread):
        def __init__(self, otp_id):
            threading.Thread.__init__(self)
            self.otp_id = otp_id

        def run(self):
            time.sleep(60 * int(otp_expire_time))
            expire_otp(self.otp_id)

    expire_otp_inner_thread(otp_id).start()


def send_otp_sms(mobile_number: str, message: str):
    Sms.sms_thread(mobile_number, message)


def send_otp_email(to: str, subject: str, message: str):
    emails.send_mail_in_thread(to, subject, message)


def validate_otp(otp_data):
    otp = otp_data.get("otp")
    verification_token = otp_data.get("verification_token")
    if not otp or not verification_token:
        return {"status": False, "message": "Invalid OTP data"}
    try:
        otp = OTP.objects.get(
            verification_token=otp_data["verification_token"], otp=otp_data["otp"]
        )
        if otp.is_expired:
            return {"status": False, "message": "OTP is expired"}
        if otp.status == OtpStatus.VERIFIED.value:
            return {"status": False, "message": "OTP is already verified"}
        else:
            otp.status = OtpStatus.VERIFIED.value
            otp.save()
            return {"status": True, "message": "OTP verified successfully"}
    except OTP.DoesNotExist:
        return {"status": False, "message": "Invalid OTP"}


def get_mobile_number(email):
    try:
        login_data = login_master.objects.get(email=email)
        return login_data.mobileNumber
    except login_master.DoesNotExist:
        return "Email is not correct"
