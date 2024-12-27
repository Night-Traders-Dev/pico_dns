import sys
sys.path.append('../../lib')
from dns_parser import parse_dns_query, create_dns_response
from custom_resolver import resolve_custom_domain
from blocklist import is_blocked
import socket
import time
import pyRTOS

UPSTREAM_DNS = "94.140.14.14"  # AdGuard DNS
CACHE_TTL = 300  # Default TTL for cache entries in seconds

# Cache structure: {domain: (response, expiration_time)}
dns_cache = {}

def get_from_cache(domain):
    """
    Retrieve a cached DNS response if it exists and is not expired.

    Args:
        domain (str): The domain name to look up in the cache.

    Returns:
        bytes: Cached DNS response or None if not found or expired.
    """
    if domain in dns_cache:
        response, expiration_time = dns_cache[domain]
        if time.time() < expiration_time:
            print(f"Cache hit for {domain}")
            return response
        else:
            print(f"Cache expired for {domain}")
            del dns_cache[domain]  # Remove expired entry
    return None

def add_to_cache(domain, response, ttl=CACHE_TTL):
    """
    Add a DNS response to the cache.

    Args:
        domain (str): The domain name to cache.
        response (bytes): The DNS response packet.
        ttl (int): Time-to-live in seconds for the cache entry.
    """
    expiration_time = time.time() + ttl
    dns_cache[domain] = (response, expiration_time)
    print(f"Added {domain} to cache with TTL {ttl} seconds.")

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
                domain = query["domain"]
                print(f"Received query for {domain} from {addr}")

                # Check if the domain is blocked
                if is_blocked(domain):
                    response = create_dns_response(query, "0.0.0.0")
                    self.sock.sendto(response, addr)
                    print(f"Blocked {domain} and returned 0.0.0.0")
                    yield [pyRTOS.timeout(self.interval)]
                    continue

                # Check the cache
                cached_response = get_from_cache(domain)
                if cached_response:
                    self.sock.sendto(cached_response, addr)
                    yield [pyRTOS.timeout(self.interval)]
                    continue

                # Check for a custom domain resolution
                ip = resolve_custom_domain(domain)
                if ip:
                    response = create_dns_response(query, ip)
                    self.sock.sendto(response, addr)
                    add_to_cache(domain, response)
                    print(f"Resolved {domain} to {ip} and cached it")
                    yield [pyRTOS.timeout(self.interval)]
                    continue

                # Forward to the upstream DNS server
                upstream_response = self.forward_to_upstream(data)
                if upstream_response:
                    self.sock.sendto(upstream_response, addr)
                    add_to_cache(domain, upstream_response)
                    print(f"Forwarded {domain} to upstream DNS and cached it")
                else:
                    print(f"Failed to resolve {domain} via upstream DNS")

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
