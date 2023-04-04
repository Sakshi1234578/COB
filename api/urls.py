from django.urls import path
from .apiView import AuthAPI
from .apiView import merchant_view
from .apiView.clientServiceAPI import profile, clientDetail, FetchAllRegisteredClients
from .apiView import CategoryAPI
from .apiView.ProductCatalogue import Product_catalogue, Product_catalogue_subdetail
from .apiView.saveSubscribeFetchAppAndPlanAPI import clientSubscribedPlan, GetSubscribedPlanDetailByClientId, \
    GetSubscribedPlanDetailsByDate
from .apiView.ZoneDetailAPI import ZoneDetails
from .apiView.BankDetailsAPI import BankDetail
from .apiView.ZoneMasterAPI import ZoneMasterDetail
from .apiView.EmployeeMasterAPI import employeeMasterDetail
from .apiView.clientServiceAPI import UpdateZoneDataClientCode, GetZoneInfoByClientCode
from .apiView.GetSettledTxnHistoryAPI import GetSettledTxnHistory, getCommonData, GetQFSettledTxnHistory, \
    GetQFWiseSettledTxnHistory
from .apiView import business_app_form_api
from .apiView.saveSubscribeFetchAppAndPlanAPI import PreUpdateSubscribedPlanDetail
urlpatterns = [
    path('auth-service/auth/signup', AuthAPI.register_api.as_view()),
    path('auth-service/auth/emailVerify/<slug:login_id>', AuthAPI.email_verify.as_view()),
    path('auth-service/auth/login', AuthAPI.login_api.as_view()),
    path('auth-service/auth/login/website-plan-detail', AuthAPI.WebsiteLoginAPI.as_view()),
    path('auth-service/client', profile.as_view()),
    # This URL is not given
    path('auth-service/updateProfile', profile.as_view()),
    # auth-service/account/forgot-password this is real url but not matching with functionality
    path('auth-service/account/getotp', AuthAPI.otp_view.as_view()),
    path('auth-service/account/verify-otp', AuthAPI.validate_otp.as_view()),
    path('auth-service/account/forgot-password', AuthAPI.forgot_password.as_view()),
    path('auth-service/account/change-password', AuthAPI.change_password.as_view()),
    path('auth-service/account/check-clientcode', AuthAPI.check_client_code.as_view()),
    path('auth-service/auth/business-category', CategoryAPI.category_api.as_view()),
    path('product/product-details', Product_catalogue.as_view()),
    path('product/product-sub-details/<slug:app_id>', Product_catalogue_subdetail.as_view()),
    path('client-subscription-service/subscribeFetchAppAndPlan', clientSubscribedPlan.as_view()),
    path('clientDetail', clientDetail.as_view()),
    path('client-subscription-service/GetSubscribedPlanDetailByClientId', GetSubscribedPlanDetailByClientId.as_view()),
    path('bank/bank-detail', BankDetail.as_view()),
    path('zone/zones-master', ZoneMasterDetail.as_view()),
    path('zone/employee-detail', employeeMasterDetail.as_view()),
    path('zone/update-zone-data', UpdateZoneDataClientCode.as_view()),
    path('zone/get-zone-info', GetZoneInfoByClientCode.as_view()),
    path('zone/zones', ZoneDetails.as_view()),
    path('merchant/get-rate-template-detail', merchant_view.RateTemplateMaster.as_view()),
    path('merchant/get-template-detail-by-business-code', merchant_view.TemplateMasterByBusinessCode.as_view()),
    path('merchant/get-risk-category-template', merchant_view.RiskCatgTemplateNameByCode.as_view()),
    path('merchant/get-signup-info', merchant_view.MerchantDetail.as_view()),
    path('merchant/checkLogin', merchant_view.CheckLogin.as_view()),
    path('merchant/update-comments', merchant_view.UpdateComment.as_view()),
    path('merchant/get-risk-business-by-id', CategoryAPI.RiskBusinessCategoryMapper.as_view()),
    path('merchant/save-comments', merchant_view.CommentSave.as_view()),
    path('merchant/get-comments-by-clientcode', merchant_view.GetComment.as_view()),
    path("merchant/rate-map", merchant_view.RateMapClone.as_view()),
    path("merchant/rate-mapping-generateClient", merchant_view.RateMappingGenerateClient.as_view()),
    path("SabPaisaReport/REST/GetSettledTxnHistory", GetSettledTxnHistory.as_view()),
    path('SabPaisaAdmin/getDataByCommonProc/getCommonData/0/0', getCommonData.as_view()),
    path("merchant/get-subscribed-details", GetSubscribedPlanDetailsByDate.as_view()),
    path("clientOnBoarding/fetchAllRegisteredClients", FetchAllRegisteredClients.as_view()),
    path("SabPaisaReport/REST/GetQFSettledTxnHistory", GetQFSettledTxnHistory.as_view()),
    path("SabPaisaReport/REST/GetQFWiseSettledTxnHistory", GetQFWiseSettledTxnHistory.as_view()),
    path("biz-app-form/", business_app_form_api.BusinessAppFormAPI.as_view()),
    path("Pre-update-subscribed-detail",PreUpdateSubscribedPlanDetail.as_view())
]
