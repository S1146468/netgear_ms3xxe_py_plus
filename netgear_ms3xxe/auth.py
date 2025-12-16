import json
from .exceptions import NetgearAPIError


class AuthManager:
    def __init__(self, transport):
        self.transport = transport
        self.token = None
        self.session_id = None

    def login(self, password: str):
        # PATCH /api/system/login
        body = json.dumps({"password": password}, separators=(",", ":"))
        r = self.transport.request(
            "PATCH",
            "/api/system/login",
            data=body,
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )
        r.raise_for_status()
        j = r.json()

        if j.get("errCode") != 0:
            raise NetgearAPIError(f"Login failed: {j}")

        self.session_id = j["id"]
        self.token = j["token"]
        self.transport.session.headers["Authorization"] = f"Bearer {self.token}"

        # POST /api/login_session
        body2 = json.dumps({"id": self.session_id, "status": True}, separators=(",", ":"))
        r2 = self.transport.request(
            "POST",
            "/api/login_session",
            data=body2,
            headers={"Content-Type": "text/plain;charset=UTF-8"},
        )

        # Known quirk: can 500 if session already exists
        if r2.status_code == 500:
            self.transport.session.cookies.clear()
            self.transport.session.headers.pop("Authorization", None)
            self.login(password)
            return

        r2.raise_for_status()
