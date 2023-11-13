import requests
import json
from requests import Response
from util.settings import settings

url = "http://127.0.0.1:8080/"


class HttpClient:

    def __init__(self, base_url: str):
        self.url = base_url
        self.auth = ""

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
                                    json=data)
            if res.status_code >= 200 and res.status_code < 300:
                return json.loads(res.text)
        except:
            return {'code': 0, 'data': None, 'msg': '请求失败'}
    
        return {'code': 0, 'data': None, 'msg': '请求失败'}
        

    def _get_full_url(self, url: str):
        if not url.startswith('/'):
            return self.url + '/' + url
        return self.url +  url
    

    
client = HttpClient(url)

def requestAPI(url: str, 
        method: str,
        data: dict|None=None):
    return client.request(url, method, data)



if __name__ == "__main__":
    res = client.get('/pet/1').data
    print(res)
    print(res.id)
    print(res.name)
    print(res.photoUrls[0])
    print(res.category.name)
