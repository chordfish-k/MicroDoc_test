import requests
from requests import Response
from dotteddict import dotteddict

url = "http://127.0.0.1:4523/m1/3340430-0-defaulta"


class HttpClient:

    def __init__(self, base_url: str):
        self.url = base_url
        self.auth = ""

    def get(self, url: str, 
        query: dict|None=None, 
        data: dict|None=None)->dotteddict:

        res = requests.get(url=self._get_full_url(url), 
                    auth=self.auth,
                    params=query,
                    data=data)
        
        if res.status_code >= 200 and res.status_code < 300:
            return dotteddict(res.json())
    
        return dotteddict({'code': 404, 'data': None, 'msg': '请求失败'})
        

    def _get_full_url(self, url: str):
        if not url.startswith('/'):
            return self.url + '/' + url
        return self.url +  url
    

    
client = HttpClient(url)

if __name__ == "__main__":
    res = client.get('/pet/1').data
    print(res)
    print(res.id)
    print(res.name)
    print(res.photoUrls[0])
    print(res.category.name)
