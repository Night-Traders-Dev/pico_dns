import sys
sys.path.append('../lib')

from custom_resolver import (
    add_custom_domain,
    remove_custom_domain,
    list_custom_domains,
    save_custom_domains_to_file,
    load_custom_domains_from_file,
)
from blocklist import (
    load_blocklist,
    save_blocklist,
    add_to_blocklist,
    remove_from_blocklist,
    list_blocked_domains,
)
from dns_server import start_dns_server
import pyRTOS


class DNSTask(pyRTOS.Task):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Starting DNS server task...")
        start_dns_server()


class BlocklistUpdateTask(pyRTOS.Task):
    def __init__(self, interval=600):  # Update every 600 seconds (10 minutes)
        super().__init__()
        self.interval = interval

    def run(self):
        while True:
            print("Updating blocklist...")
            load_blocklist("blocklist.txt")  # Re-load the blocklist dynamically
            yield [pyRTOS.timeout(self.interval)]


class CLIHandler:
    def __init__(self):
        self.running = True

    def handle_command(self, command):
        if not command:
            return

        cmd = command[0]
        if cmd == "add" and len(command) == 3:
            domain, ip = command[1], command[2]
            add_custom_domain(domain, ip)
        elif cmd == "remove" and len(command) == 2:
            domain = command[1]
            remove_custom_domain(domain)
        elif cmd == "list_domains":
            print("Custom domains:")
            for domain, ip in list_custom_domains().items():
                print(f"{domain} -> {ip}")
        elif cmd == "save_domains":
            save_custom_domains_to_file("custom_domains.json")
        elif cmd == "load_domains":
            load_custom_domains_from_file("custom_domains.json")
        elif cmd == "block" and len(command) == 2:
            domain = command[1]
            add_to_blocklist(domain)
        elif cmd == "unblock" and len(command) == 2:
            domain = command[1]
            remove_from_blocklist(domain)
        elif cmd == "list_blocked":
            print("Blocked domains:")
            for domain in list_blocked_domains():
                print(domain)
        elif cmd == "save_blocklist":
            save_blocklist("blocklist.txt")
        elif cmd == "start":
            print("The DNS server is already running in a task.")
        elif cmd == "exit":
            print("Exiting DNS Server CLI.")
            self.running = False
        else:
            print("Invalid command.")

    def run_cli(self):
        print("DNS Server CLI")
        print("Commands:")
        print("  add <domain> <ip>       - Add a custom domain")
        print("  remove <domain>         - Remove a custom domain")
        print("  list_domains            - List all custom domains")
        print("  save_domains            - Save custom domains to a file")
        print("  load_domains            - Load custom domains from a file")
        print("  block <domain>          - Block a domain")
        print("  unblock <domain>        - Unblock a domain")
        print("  list_blocked            - List all blocked domains")
        print("  save_blocklist          - Save the blocklist to a file")
        print("  start                   - Start the DNS server")
        print("  exit                    - Exit the CLI")

        while self.running:
            try:
                command = input("> ").strip().split()
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\nExiting DNS Server CLI.")
                self.running = False


class CLITask(pyRTOS.Task):
    def __init__(self):
        super().__init__()

    def run(self):
        cli = CLIHandler()
        cli.run_cli()


def main():
    # Load the initial blocklist and custom domains
    load_blocklist("blocklist.txt")
    load_custom_domains_from_file("custom_domains.json")

    # Add pyRTOS tasks
    pyRTOS.add_task(DNSTask())
    pyRTOS.add_task(BlocklistUpdateTask())
    pyRTOS.add_task(CLITask())

    # Start the RTOS
    pyRTOS.start()


if __name__ == "__main__":
    main()
