import requests


class Transport:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Referer": self.base + "/",
            "Origin": self.base,
        })

    def request(self, method: str, path: str, **kwargs):
        url = self.base + path
        return self.session.request(method, url, timeout=self.timeout, **kwargs)
