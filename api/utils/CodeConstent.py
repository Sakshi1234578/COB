from enum import Enum


class codeConstant(Enum):
    user_exist = "User Already Exist"
    User_registered = "User successfully registered. Please check your mail for verification"
    Username_password_blank_null = "Username and password blank or null"
    user_Email_not_verified = "Email id not verified"
    user_name_email_not_correct = "user name or email not correct"
    client_code_must_be_unique = "client code must be unique"
    regex = (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    email_required = "Email required"
    Email_not_valid = "Email is not valid"
    Mobile_number_required = "mobile number is required"
    Mobile_error = "Mobile number should be equal 10 digit"
    Name_required = "Name required"
    Password_required = "Password required"
    INDIVIDUAL = "individual_clientType"
    BUSINESS = "business_clientType"
    Business_category = "Business Category Code is required"
    user_register = "Data Inserted Successfully"
