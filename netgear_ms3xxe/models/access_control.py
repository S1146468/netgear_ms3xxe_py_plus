from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network


@dataclass(frozen=True)
class AccessRuleIP:
    ip: str
    mask: str

    def validate(self):
        IPv4Address(self.ip)
        IPv4Network(f"{self.ip}/{self.mask}", strict=False)
