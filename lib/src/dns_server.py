import sys
sys.path.append('../../lib')
from dns_parser import parse_dns_query, create_dns_response
from custom_resolver import resolve_custom_domain
from blocklist import is_blocked
import socket
import pyRTOS

UPSTREAM_DNS = "94.140.14.14"  # AdGuard DNS


class DNSServerTask(pyRTOS.Task):
    def __init__(self, interval=0):
        """
        Initialize the DNS server task.

        Args:
            interval (int): Interval between task yields (default 0 for immediate).
        """
        super().__init__()
        self.interval = interval
        self.sock = None

    def forward_to_upstream(self, query):
        """
        Forward the DNS query to the upstream DNS server.

        Args:
            query (bytes): The raw DNS query packet.

        Returns:
            bytes: The raw DNS response packet from the upstream server.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(query, (UPSTREAM_DNS, 53))
                response, _ = sock.recvfrom(512)
            return response
        except socket.timeout:
            print("Upstream DNS server timed out.")
            return None
        except Exception as e:
            print(f"Error forwarding to upstream DNS: {e}")
            return None

    def run(self):
        """
        Run the DNS server task.
        """
        # Initialize the socket for the DNS server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 53))
        print("DNS server is running on port 53...")

        while True:
            try:
                # Receive a DNS query
                data, addr = self.sock.recvfrom(512)
                query = parse_dns_query(data)
                print(f"Received query for {query['domain']} from {addr}")

                # Check if the domain is blocked
                if is_blocked(query["domain"]):
                    response = create_dns_response(query, "0.0.0.0")
                    self.sock.sendto(response, addr)
                    print(f"Blocked {query['domain']} and returned 0.0.0.0")
                    yield [pyRTOS.timeout(self.interval)]
                    continue

                # Check for a custom domain resolution
                ip = resolve_custom_domain(query["domain"])
                if ip:
                    response = create_dns_response(query, ip)
                    self.sock.sendto(response, addr)
                    print(f"Resolved {query['domain']} to {ip}")
                    yield [pyRTOS.timeout(self.interval)]
                    continue

                # Forward to the upstream DNS server
                upstream_response = self.forward_to_upstream(data)
                if upstream_response:
                    self.sock.sendto(upstream_response, addr)
                    print(f"Forwarded {query['domain']} to upstream DNS")
                else:
                    print(f"Failed to resolve {query['domain']} via upstream DNS")

            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"Error: {e}")

            # Yield control to other tasks
            yield [pyRTOS.timeout(self.interval)]

    def close(self):
        """
        Close the DNS server socket.
        """
        if self.sock:
            self.sock.close()
            print("DNS server socket closed.")
