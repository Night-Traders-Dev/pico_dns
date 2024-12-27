# MicroPython DNS Server with Ad Blocking

This project implements a lightweight DNS server that runs on the Raspberry Pi Pico W using MicroPython. It features native ad blocking via a customizable blocklist and integrates with AdGuard DNS for enhanced filtering. Additionally, the server supports custom domain mappings for flexible DNS management.

---

## Features

- **DNS Server**: Listens on port 53 for DNS queries.
- **Ad Blocking**:
  - Intercepts requests for domains in the blocklist and returns a local IP (e.g., `0.0.0.0`).
  - Includes a sample blocklist with known ad-serving domains.
- **Custom Domain Mappings**:
  - Define custom IP addresses for specific domains (e.g., `example.com -> 192.168.1.100`).
- **Upstream DNS Resolution**:
  - Forwards unresolved queries to AdGuard DNS (`94.140.14.14`) or any other upstream server.
- **Dynamic Updates**:
  - Add or remove custom domains and blocklist entries at runtime via the CLI.

---


## Installation

### 1. Prerequisites

- **Hardware**: Raspberry Pi Pico W
- **Software**:
  - MicroPython firmware installed on the Pico W ([Guide](https://micropython.org/download/rp2-pico-w/))
  - A serial terminal or file transfer tool (e.g., `mpfshell`, `ampy`).

---

### 2. Setup

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/Night-Traders-Dev/pico_dns.git
   cd pico_dns
   ```

2. **Transfer Files to Pico W**:

Copy the lib/ and src/ directories to your Pico W.

```bash
mpfshell
mput lib/*
mput src/main.py
```

3. **Create a Blocklist File**:

Add a file named blocklist.txt on the Pico W with domains to block.


# Example blocklist
```bash
ads.google.com
doubleclick.net
adservice.google.com
```



---

**Usage**

*Start the CLI*

1. *Open a serial terminal to the Pico W*.


2. *Run main.py to access the DNS server CLI*.


```bash
PicoW> python src/main.py
```

---

**Commands**


---

**Examples**

*Add a Custom Domain Mapping*

```bash
> add example.com 192.168.1.100
```

*Block a Domain*

```bash
> block ads.google.com
```

*Unblock a Domain*

```bash
> unblock ads.google.com
```

*Start the DNS Server*

```bash
> start
```

*Exit the CLI*

```bash
> exit
```

---

**How It Works**

1. *DNS Query Handling*:

Incoming DNS queries are parsed to extract the domain name.

The server checks:

1. *Blocklist: If the domain is blocked, 0.0.0.0 is returned*.


2. *Custom Resolver: If a custom mapping exists, the corresponding IP is returned*.


3. *Upstream DNS: If unresolved, the query is forwarded to AdGuard DNS*.





2. *Ad Blocking*:

Requests to ad-serving domains in the blocklist are intercepted and resolved to 0.0.0.0, preventing ads from being served.





---

**Blocklist Management**

*Default Blocklist*:

Add domains to blocklist.txt for ad blocking.

*Example*:

```bash
ads.google.com
doubleclick.net
adservice.google.com
```

**Dynamic Updates**:

Use the block and unblock commands in the CLI to modify the blocklist at runtime.




---

**Customization**

1. *Change Upstream DNS*:

```bash
Edit the UPSTREAM_DNS variable in dns_server.py to use a different DNS server.

UPSTREAM_DNS = "8.8.8.8"  # Google DNS
```


2. *Modify Blocklist*:

Update blocklist.txt or use the CLI commands.



3. *Logging*:

Extend the logging functionality in dns_server.py for more detailed logs.





---

**Troubleshooting**

1. *Port 53 Binding Error*:

Ensure no other services are using port 53.



2. *DNS Not Resolving*:

Verify your blocklist and custom mappings.

Check the upstream DNS server configuration.





---

**Disclaimer**
```bash
This project is for educational purposes only. Use responsibly and only on networks you own or have explicit permission to operate on.
```

---

**License**

This project is licensed under the MIT License.
