from rest_framework import status


class CustomException(Exception):
    """
    Base class for all custom exceptions
    """
    message = None
    status_code = None
    detail = None

    def __init__(self, detail=None, message=None, status_code=None):
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail


class UserAlreadyExistException(CustomException):
    message = "User Already Exist"
    status_code = status.HTTP_409_CONFLICT


class UserNotExistException(CustomException):
    message = "User Not Exist"
    status_code = status.HTTP_409_CONFLICT


class PassNotExistException(CustomException):
    message = "Password is Incorrect"
    status_code = status.HTTP_409_CONFLICT


class VerifyUserFirst(CustomException):
    message = "Email Is Not Verified, Verify Your Email First"
    status_code = status.HTTP_400_BAD_REQUEST


class MobileNumberAlreadyExist(CustomException):
    message = "Mobile Number Already Exist"
    status_code = status.HTTP_409_CONFLICT


class UnauthorizedException(CustomException):
    message = "Not Unauthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class IncompleteDataException(CustomException):
    message = "Incomplete Data"
    status_code = status.HTTP_400_BAD_REQUEST


class MailNotVerifiedException(CustomException):
    message = "Email Not Verified"
    status_code = status.HTTP_401_UNAUTHORIZED


class ClientTypeNotCorrect(CustomException):
    message = "Client Type Is Not Correct"
    status_code = status.HTTP_400_BAD_REQUEST


class ClientCodeNotCorrect(CustomException):
    message = "Client Code is Not Correct"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailNotCorrect(CustomException):
    message = "Email is Incorrect"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailAlreadyExist(CustomException):
    message = "Email Already Exist"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailIDNotCorrect(CustomException):
    message = "Check Your Email"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailNotVerified(CustomException):
    message = "Verify Your Email"
    status_code = status.HTTP_400_BAD_REQUEST


class BlankData(CustomException):
    message = "Provide All Data"
    status_code = status.HTTP_404_NOT_FOUND


class StateNameNotCorrect(CustomException):
    message = "State Name Is Incorrect"
    status_code = status.HTTP_400_BAD_REQUEST


class ProfileNotCreate(CustomException):
    message = "Profile Not Created"
    status_code = status.HTTP_400_BAD_REQUEST


class ProfileAlreadyCreate(CustomException):
    message = "Profile Already Created"
    status_code = status.HTTP_400_BAD_REQUEST


class IntegerFieldRequired(CustomException):
    message = "Please send number"
    status_code = status.HTTP_400_BAD_REQUEST


class SubscriptionAlreadyExist(CustomException):
    message = "Plan already subscribed"
    status_code = status.HTTP_400_BAD_REQUEST


class DataNotFound(CustomException):
    message = "Data Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class ClientCodeNotFound(CustomException):
    message = "Client Code Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class DateFormat(CustomException):
    message = "Date Format is Not Supported"
    status_code = status.HTTP_404_NOT_FOUND

class InvalidFormatException(CustomException):
    message = "Invalid Syntax"
    status=status.HTTP_400_BAD_REQUEST

class InvalidDataException(CustomException):
    message = "Invalid Data"
    status = status.HTTP_400_BAD_REQUEST