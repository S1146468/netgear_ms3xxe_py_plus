from ..models.ports import PortConf


class PortsAPI:
    def __init__(self, router):
        self.router = router

    def get(self):
        j = self.router.get("/api/ports")
        return [
            PortConf(
                port_no=p["portNo"],
                name=p.get("portName", ""),
                link_speed_conf=p["linkSpeedConf"],
                link_speed=p["linkSpeed"],
                flow_control=p["flowControl"],
            )
            for p in j["portConfs"]
        ]
