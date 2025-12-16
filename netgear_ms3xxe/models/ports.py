from dataclasses import dataclass


@dataclass(frozen=True)
class PortConf:
    port_no: int
    name: str
    link_speed_conf: str
    link_speed: str
    flow_control: bool
