from dns_parser import parse_dns_query, create_dns_response
from custom_resolver import resolve_custom_domain
from blocklist import is_blocked, load_blocklist
import socket

UPSTREAM_DNS = "94.140.14.14"  # AdGuard DNS

def forward_to_upstream(query):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(query, (UPSTREAM_DNS, 53))
        response, _ = sock.recvfrom(512)
    return response

def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53))
    print("DNS server is running on port 53...")

    while True:
        try:
            data, addr = sock.recvfrom(512)
            query = parse_dns_query(data)
            print(f"Received query for {query['domain']} from {addr}")

            if is_blocked(query["domain"]):
                response = create_dns_response(query, "0.0.0.0")
                sock.sendto(response, addr)
                print(f"Blocked {query['domain']} and returned 0.0.0.0")
                continue

            ip = resolve_custom_domain(query["domain"])
            if ip:
                response = create_dns_response(query, ip)
                sock.sendto(response, addr)
                print(f"Resolved {query['domain']} to {ip}")
            else:
                response = forward_to_upstream(data)
                sock.sendto(response, addr)
                print(f"Forwarded {query['domain']} to upstream DNS")
        except Exception as e:
            print(f"Error: {e}")
