from ..models.access_control import AccessRuleIP


class AccessControlAPI:
    def __init__(self, router):
        self.router = router

    def get(self):
        j = self.router.api("GET", "/api/system/settings/accesscontrol")
        return [AccessRuleIP(ip=r["ipAddr"], mask=r["mask"]) for r in j["accessConfs"]]
