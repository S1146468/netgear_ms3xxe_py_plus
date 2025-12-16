import json
from .exceptions import NetgearAPIError


class Router:
    def __init__(self, transport, auth):
        self.transport = transport
        self.auth = auth

    def api(self, method: str, path: str, *, text_json=None):
        r = self.transport.request(
            method,
            path,
            data=json.dumps(text_json, separators=(",", ":")) if text_json else None,
            headers={"Content-Type": "text/plain;charset=UTF-8"} if text_json else None,
        )

        if r.status_code == 401:
            raise NetgearAPIError("Unauthorized")

        r.raise_for_status()

        j = r.json()
        if "errCode" in j and j["errCode"] not in (0, None):
            raise NetgearAPIError(j)

        return j
