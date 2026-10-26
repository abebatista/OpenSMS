import socket

# OS specific
try:
    from kivy.utils import platform
except ImportError:
    import sys
    if sys.platform.startswith("win"):
        platform = "win"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    else:
        platform = "unknown"

# Get the Local IPs which have Internet connection
def get_internet_iface_ips():
    ip_addresses = []

    for target in [('8.8.8.8', 80), ('1.1.1.1', 80)]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.2)
            s.connect(target)
            ip = s.getsockname()[0]
            s.close()
            if ip not in ip_addresses and not ip.startswith('127.'):
                ip_addresses.append(ip)
        except Exception as e:
            print(f"Error while fetching IPs: {e}")

    return ip_addresses

def get_network_ips():
    lan_ips = {"wifi": [], "ethernet": []}
    try:
        if platform == "android":
            from jnius import autoclass
            NetworkInterface = autoclass('java.net.NetworkInterface')
            interfaces = NetworkInterface.getNetworkInterfaces()
            if interfaces:
                while interfaces.hasMoreElements():
                    net_if = interfaces.nextElement()
                    if not net_if.isUp() or net_if.isLoopback():
                        continue
                    iface_name = str(net_if.getName()).lower()
                    addrs = net_if.getInetAddresses()
                    while addrs.hasMoreElements():
                        addr = addrs.nextElement()
                        ip_addr = str(addr.getHostAddress()).strip()
                        if "%" in ip_addr:
                            ip_addr = ip_addr.split("%")[0]
                        # Taking IPv4 only
                        if not ip_addr.startswith("127.") and ":" not in ip_addr:
                            iface_type = (
                                "wifi" if any(k in iface_name for k in ["wlan", "wl", "wifi"]) else (
                                "cellular" if any(k in iface_name for k in ["rmnet", "ccmni", "pdp", "wwan"]) else (
                                "ethernet" if any(k in iface_name for k in ["eth", "en"]) else "lan"
                            )))
                            if iface_type == "wifi":
                               lan_ips["wifi"].append({"interface": iface_name, "ip": ip_addr})
                            elif iface_type in ["ethernet", "lan"]:
                               lan_ips["ethernet"].append({"interface": iface_name, "ip": ip_addr})
        else:
           lan_ips = get_desktop_lan_ips()

    except Exception as e:
       print(f"Error in fetching IPs: {e}")

    return lan_ips

# Get the LAN IPs from desktop platform
def get_desktop_lan_ips():
    import psutil
    lan_ips = {"wifi": [], "ethernet": []}

    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface_name, iface in addrs.items():
        # Check if the interface is actually active/up
        if iface_name in stats and not stats[iface_name].isup:
            continue

        # Filter out virtual, loopback, docker, VPN, and tunnel adapters by name keywords
        lower_name = iface_name.lower()
        if any(
            keyword in lower_name
            for keyword in [
                "loopback",
                "lo",
                "pseudo",
                "docker",
                "veth",
                "br-",
                "vmware",
                "virtualbox",
                "tap",
                "radmin",
            ]
        ):
            continue

        # Look for IPv4 addresses
        if iface[0].family == socket.AF_INET:
            ip = iface[0].address
            if ip.startswith("127."):
                continue

            iface_type = (
                "wifi" if any(k in iface_name for k in ["wlan", "wl", "wifi"]) else (
                "ethernet" if any(k in iface_name for k in ["eth", "en"]) else "lan"
            ))

            if iface_type == "wifi":
               lan_ips["wifi"].append({"interface": iface_name, "ip": ip})
            elif iface_type in ["ethernet", "lan"]:
               lan_ips["ethernet"].append({"interface": iface_name, "ip": ip})

    return lan_ips

