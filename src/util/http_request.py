import requests
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray, QJsonDocument
import json
from src.util.settings import settings
from src.util.logger import logger

url = "http://{}:{}/".format(settings.get("server"), settings.get("port"))

class Client:
    session = None

    def __init__(self, base_url: str):
        self.url = base_url

    def request(self, 
            url: str, 
            method: str,
            data: dict|None=None):
        pass

    def _get_full_url(self, url: str):
        if not url.startswith('/'):
            return self.url + '/' + url
        return self.url +  url


class HttpClient(Client):
    
    def __init__(self, base_url: str=""):
        super().__init__(base_url)


    def request(self, 
            url: str, 
            method: str,
            data: dict|None=None):

        token = settings.get("token")

        try:
            res = requests.request(url=self._get_full_url(url), 
                                    headers={
                                        'Content-Type':'application/json',
                                        'token': token
                                    },
                                    method=method,
                                    json=data,
                                    timeout=1000)
            if res.status_code >= 200 and res.status_code < 300:
                return json.loads(res.text)
        except Exception as e:
            logger.error(e)
            return {'code': 0, 'data': None, 'msg': '请求失败 '}
        
        return {'code': 0, 'data': None, 'msg': '请求失败 '}
        

class QClient(Client):

    def __init__(self, base_url: str=""):
        super().__init__(base_url)
        self.manager = QNetworkAccessManager()


    def request(self, url: str, method: str, data: dict | None = None):
        req = QNetworkRequest(QUrl(self._get_full_url(url)))
        req.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, QByteArray('application/json'))
        req.setRawHeader(QByteArray("token"), QByteArray(token = settings.get("token")))
        self.manager.sendCustomRequest(request=req, 
                                       verb=QByteArray(method), 
                                       data=QJsonDocument(data).toJson(QJsonDocument.JsonFormat.Compact))
        self.manager.finished.connect(self.finish)


    def finish(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            bytes: QByteArray = reply.readAll()
            jsonDoc: QJsonDocument = QJsonDocument.fromJson(bytes)
            obj = jsonDoc.object()
        
        reply.deleteLater()
    

client:Client = HttpClient(url)

def requestAPI(url: str, 
        method: str,
        data: dict|None=None):

    return client.request(url=url, method=method, data=data)


if __name__ == "__main__":
    res = client.get('/pet/1').data
    print(res)
    print(res.id)
    print(res.name)
    print(res.photoUrls[0])
    print(res.category.name)
