from .transport import Transport
from .auth import AuthManager
from .router import Router
from .domains.ports import PortsAPI
from .domains.access_control import AccessControlAPI


class NetgearSwitchClient:
    def __init__(self, host: str, password: str):
        self.transport = Transport(f"http://{host}")
        self.auth = AuthManager(self.transport)
        self.auth.login(password)

        self.router = Router(self.transport, self.auth)

        self.ports = PortsAPI(self.router)
        self.access_control = AccessControlAPI(self.router)
