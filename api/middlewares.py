import json


def log_request(get_response):
    def middleware(request):
        
        if request.path =='/SabPaisaReport/REST/GetSettledTxnHistory' or request.path =='/SabPaisaReport/REST/GetQFSettledTxnHistory':
            response = get_response(request)
            return response
        else:
            try:
                print("======================= Request body =======================")
                print("Request path : ", request.path)
                print("Request method : ", request.method)
                print("Request content_type : ", request.content_type)
                if request.content_type == 'text/plain':
                    print("No Body Found....")
                elif request.content_type == 'multipart/form-data':
                    print("Body in form data")
                else:
                    print("Request Body: ", json.loads(request.body))

                print("======================= Request headers =======================")
                print("client ip address : ", request.META.get('REMOTE_ADDR'))
                print("Http user : ", request.META['HTTP_USER_AGENT'])
                print("Request COOKIES : ", request.COOKIES)
                print("Request user : ", request.user)
                print("Request content_params : ", request.content_params)
                print("Request is_secure : ", request.is_secure)
                print("Request session : ", request.session)
                
            except Exception:
                import traceback
                traceback.print_exc()
            response = get_response(request)
            response_body = None
            if response and response["content-type"] == "application/json":
                response_body = json.loads(response.content.decode("utf-8"))
            print("Response data :", json.dumps(response_body, indent=4))
            return response

    return middleware
