from src.util.http_request import requestAPI

def getReportListAPI():
    return requestAPI("report", "GET")

def getReportPageAPI(page, pageSize):
    return requestAPI("report/page?page={}&pageSize={}".format(page, pageSize), 
                      "GET")

def postReportAPI(data):
    return requestAPI("report", "POST", data)