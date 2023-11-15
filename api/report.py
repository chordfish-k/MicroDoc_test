from util.http_request import requestAPI

def getReportListAPI():
    return requestAPI("report", "GET")

def postReportAPI(data):
    return requestAPI("report", "POST", data)