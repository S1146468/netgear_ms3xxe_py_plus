from netgear_ms3xxe.client import NetgearSwitchClient

sw = NetgearSwitchClient("192.168.2.251", "YOURpassword1234!")

for p in sw.ports.get():
    print(p)

print(sw.access_control.get())
