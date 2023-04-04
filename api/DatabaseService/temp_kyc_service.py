from api.databaseModels.temp_kyc import TempKyc


def create_temp_kyc(login_id, name, number, email):
    temp_kyc = TempKyc(login_id=login_id, name=name,
                       number=number, email=email)
    temp_kyc.save()
    return temp_kyc
