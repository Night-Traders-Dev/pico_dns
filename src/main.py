import sys
sys.path.append('../lib')
from custom_resolver import add_custom_domain, remove_custom_domain
from blocklist import load_blocklist, add_to_blocklist, remove_from_blocklist
from dns_server import start_dns_server

def main():
    load_blocklist("blocklist.txt")

    print("DNS Server CLI")
    print("Commands:")
    print("  add <domain> <ip>    - Add a custom domain")
    print("  remove <domain>      - Remove a custom domain")
    print("  block <domain>       - Block a domain")
    print("  unblock <domain>     - Unblock a domain")
    print("  start                - Start the DNS server")
    print("  exit                 - Exit the CLI")

    while True:
        command = input("> ").strip().split()
        if not command:
            continue

        cmd = command[0]
        if cmd == "add" and len(command) == 3:
            domain, ip = command[1], command[2]
            add_custom_domain(domain, ip)
        elif cmd == "remove" and len(command) == 2:
            domain = command[1]
            remove_custom_domain(domain)
        elif cmd == "block" and len(command) == 2:
            domain = command[1]
            add_to_blocklist(domain)
        elif cmd == "unblock" and len(command) == 2:
            domain = command[1]
            remove_from_blocklist(domain)
        elif cmd == "start":
            start_dns_server()
        elif cmd == "exit":
            print("Exiting DNS Server CLI.")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
