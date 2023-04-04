from enum import Enum


class OtpStatus(Enum):
    PENDING = "Pending"
    VERIFIED = "Verified"
    EXPIRED = "Expired"


class OtpType(Enum):
    PHONE = "Phone"
    EMAIL = "Email"
    BOTH = "Both"

class OtpFor(Enum):
    UPDATE_PASSWORD = "Update Password"
    FORGOT_PASSWORD = "Forgot Password"


