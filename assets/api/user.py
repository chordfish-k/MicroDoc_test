from util.http_request import requestAPI


def postUserLoginAPI(data):
    """
    data:
        phone:str
        pwd:str
    """
    print(data)
    return requestAPI("user/login", "POST", data)


def getUserTestAPI():
    return requestAPI("user/test", "GET")