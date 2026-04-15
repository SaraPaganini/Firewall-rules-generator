import ipaddress

def validate_ip(source):
    try:
        ipaddress.ip_network(source, strict=False)
        return True
    except:
        return False

def generate_rule(proto, port, source, action, target):
    if not validate_ip(source):
        return "Errore: IP sorgente non valido."
    
    proto_lower = proto.lower()
    if target == "iptables":
        return f"iptables -A INPUT -p {proto_lower} -s {source} --dport {port} -j {action}"
    elif target == "nftables":
        if proto_lower == "icmp":
            return f"nft add rule inet filter input ip protocol icmp ip saddr {source} counter {action.lower()}"
        dport_match = f"{proto_lower} dport {port}" if proto_lower != "icmp" else ""
        return f"nft add rule inet filter input ip protocol {proto_lower} {dport_match} ip saddr {source} counter {action.lower()}"
    elif target == "Cisco ASA":
        return f"access-list outside_access_in extended permit {proto_lower} {source} eq {port} any"
    return "Sintassi non implementata."