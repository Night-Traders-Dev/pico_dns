import sys
import uasyncio as asyncio
sys.path.append('../../lib')
from dns_parser import parse_dns_query, create_dns_response, create_error_response
from custom_resolver import resolve_custom_domain
from blocklist import is_blocked
import socket
import time
import json

UPSTREAM_DNS = "94.140.14.14"  # AdGuard DNS
CACHE_TTL = 300  # Default TTL for cache entries in seconds
CACHE_FILE = "dns_cache.json"

# Cache structure: {domain: (response, expiration_time)}
dns_cache = {}


def load_cache():
    """
    Load DNS cache from a file.
    """
    global dns_cache
    try:
        with open(CACHE_FILE, "r") as file:
            raw_cache = json.load(file)
            dns_cache = {
                domain: (response, time.time() + ttl)
                for domain, (response, ttl) in raw_cache.items()
            }
        print(f"Cache loaded with {len(dns_cache)} entries.")
    except FileNotFoundError:
        print("Cache file not found. Starting with an empty cache.")
    except Exception as e:
        print(f"Error loading cache: {e}")


def save_cache():
    """
    Save DNS cache to a file.
    """
    try:
        with open(CACHE_FILE, "w") as file:
            raw_cache = {
                domain: (response, max(0, expiration_time - time.time()))
                for domain, (response, expiration_time) in dns_cache.items()
                if expiration_time > time.time()
            }
            json.dump(raw_cache, file)
        print(f"Cache saved with {len(raw_cache)} entries.")
    except Exception as e:
        print(f"Error saving cache: {e}")


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


async def forward_to_upstream(query):
    """
    Forward the DNS query to the upstream DNS server.

    Args:
        query (bytes): The raw DNS query packet.

    Returns:
        bytes: The raw DNS response packet from the upstream server.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    finally:
        sock.close()


async def handle_request(data, addr, sock):
    """
    Handle a single DNS request.

    Args:
        data (bytes): The raw DNS query data.
        addr (tuple): The client address.
        sock (socket): The server socket.
    """
    query = parse_dns_query(data)
    if not query:
        print("Failed to parse query.")
        return

    domain = query["domain"]
    print(f"Received query for {domain} from {addr}")

    # Check if the domain is blocked
    if is_blocked(domain):
        response = create_dns_response(query, "0.0.0.0")
        sock.sendto(response, addr)
        print(f"Blocked {domain} and returned 0.0.0.0")
        return

    # Check the cache
    cached_response = get_from_cache(domain)
    if cached_response:
        sock.sendto(cached_response, addr)
        return

    # Check for a custom domain resolution
    ip = resolve_custom_domain(domain)
    if ip:
        response = create_dns_response(query, ip)
        sock.sendto(response, addr)
        add_to_cache(domain, response)
        print(f"Resolved {domain} to {ip} and cached it")
        return

    # Forward to the upstream DNS server
    upstream_response = await forward_to_upstream(data)
    if upstream_response:
        sock.sendto(upstream_response, addr)
        add_to_cache(domain, upstream_response)
        print(f"Forwarded {domain} to upstream DNS and cached it")
    else:
        print(f"Failed to resolve {domain} via upstream DNS")


async def start_dns_server():
    """
    Start the DNS server to listen for queries on UDP port 53.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53))
    print("DNS server is running on port 53...")

    load_cache()

    try:
        while True:
            data, addr = sock.recvfrom(512)
            asyncio.create_task(handle_request(data, addr, sock))
    except KeyboardInterrupt:
        print("Shutting down DNS server.")
    finally:
        save_cache()
        sock.close()
