# MicroPython DNS Server with Ad Blocking and Caching

This project implements a lightweight DNS server that runs on the Raspberry Pi Pico W using MicroPython. It features native ad blocking via a customizable blocklist, integrates with AdGuard DNS for enhanced filtering, and includes a caching mechanism to improve performance by storing recently resolved queries. The server also supports custom domain mappings for flexible DNS management.

---

## Features

- **DNS Server**:
  - Listens on port 53 for DNS queries.
- **Ad Blocking**:
  - Intercepts requests for domains in the blocklist and returns a local IP (e.g., `0.0.0.0`).
  - Includes a sample blocklist with known ad-serving domains.
- **Custom Domain Mappings**:
  - Define custom IP addresses for specific domains (e.g., `example.com -> 192.168.1.100`).
- **Caching**:
  - Stores recently resolved domains to improve response time for repeated queries.
  - Includes a Time-to-Live (TTL) mechanism for cache expiration.
  - Supports persistent caching via `dns_cache.json`.
- **Cache Management**:
  - View, clear, or reset the cache using CLI commands.
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
   Copy the `lib/` and `src/` directories to your Pico W.
   ```bash
   mpfshell
   mput lib/*
   mput src/main.py
   ```

3. **Create Supporting Files**:
   - **Blocklist File**: Add a file named `blocklist.txt` on the Pico W with domains to block.
     ```plaintext
     # Example blocklist
     ads.google.com
     doubleclick.net
     adservice.google.com
     ```
   - **DNS Cache File**: Add an empty `dns_cache.json` file to the root directory.
     ```json
     {}
     ```

---

## Usage

### Start the CLI

1. Open a serial terminal to the Pico W.
2. Run `main.py` to access the DNS server CLI:
   ```bash
   PicoW> python src/main.py
   ```

---

### CLI Commands

| Command                 | Description                                   |
|-------------------------|-----------------------------------------------|
| `add <domain> <ip>`     | Add a custom domain mapping.                  |
| `remove <domain>`       | Remove a custom domain mapping.               |
| `list_domains`          | List all custom domain mappings.              |
| `block <domain>`        | Block a domain.                               |
| `unblock <domain>`      | Unblock a domain.                             |
| `list_blocked`          | List all blocked domains.                     |
| `save_blocklist`        | Save the current blocklist to a file.         |
| `save_domains`          | Save custom domains to a file.                |
| `load_domains`          | Load custom domains from a file.              |
| `view_cache`            | Display the current DNS cache.                |
| `clear_cache`           | Clear all entries in the DNS cache.           |
| `start`                 | Start the DNS server.                         |
| `exit`                  | Exit the CLI.                                 |

---

### Examples

1. **Add a Custom Domain Mapping**:
   ```bash
   > add example.com 192.168.1.100
   ```
2. **Block a Domain**:
   ```bash
   > block ads.google.com
   ```
3. **View Cache**:
   ```bash
   > view_cache
   ```
4. **Clear Cache**:
   ```bash
   > clear_cache
   ```
5. **Start the DNS Server**:
   ```bash
   > start
   ```
6. **Exit the CLI**:
   ```bash
   > exit
   ```

---

## How It Works

### 1. DNS Query Handling:
- **Incoming DNS queries** are parsed to extract the domain name.
- The server checks:
  1. **Cache**: If the domain is cached and valid, the cached response is returned.
  2. **Blocklist**: If the domain is blocked, `0.0.0.0` is returned.
  3. **Custom Resolver**: If a custom mapping exists, the corresponding IP is returned.
  4. **Upstream DNS**: If unresolved, the query is forwarded to AdGuard DNS.

### 2. Ad Blocking:
- Requests to ad-serving domains in the blocklist are intercepted and resolved to `0.0.0.0`, preventing ads from being served.

### 3. Caching:
- Recently resolved domains are stored in a cache to speed up repeated queries.
- Cached entries expire after the specified TTL (default: 300 seconds).
- Cache is persisted in `dns_cache.json` to survive server restarts.

---

## Blocklist Management

### Default Blocklist:
- Add domains to `blocklist.txt` for ad blocking.
- Example:
  ```plaintext
  ads.google.com
  doubleclick.net
  adservice.google.com
  ```

### Dynamic Updates:
- Use the `block` and `unblock` commands in the CLI to modify the blocklist at runtime.

---

## Customization

1. **Change Upstream DNS**:
   - Edit the `UPSTREAM_DNS` variable in `dns_server.py`:
     ```python
     UPSTREAM_DNS = "8.8.8.8"  # Google DNS
     ```

2. **Modify Blocklist**:
   - Update `blocklist.txt` or use the CLI commands.

3. **Cache Management**:
   - Use CLI commands (`view_cache`, `clear_cache`) to manage the DNS cache.

4. **Logging**:
   - Extend the logging functionality in `dns_server.py` for more detailed logs.

---

## Troubleshooting

1. **Port 53 Binding Error**:
   - Ensure no other services are using port 53.

2. **DNS Not Resolving**:
   - Verify your blocklist and custom mappings.
   - Check the upstream DNS server configuration.

3. **Cache Issues**:
   - Ensure `dns_cache.json` exists and is writable.

---

## Disclaimer

This project is for educational purposes only. Use responsibly and only on networks you own or have explicit permission to operate on.

---

## License

This project is licensed under the MIT License.
