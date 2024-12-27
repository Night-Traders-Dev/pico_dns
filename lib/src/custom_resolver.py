import json

custom_domains = {}

def add_custom_domain(domain, ip):
    """
    Add a custom domain mapping.

    Args:
        domain (str): The domain name.
        ip (str): The IP address to map to.
    """
    custom_domains[domain] = ip
    print(f"Added custom domain: {domain} -> {ip}")

def remove_custom_domain(domain):
    """
    Remove a custom domain mapping.

    Args:
        domain (str): The domain name to remove.
    """
    if domain in custom_domains:
        del custom_domains[domain]
        print(f"Removed custom domain: {domain}")
    else:
        print(f"Domain {domain} not found.")

def resolve_custom_domain(domain):
    """
    Resolve a domain using custom mappings, with support for exact and wildcard matches.

    Args:
        domain (str): The domain name.

    Returns:
        str: The resolved IP address or None if not found.
    """
    # Exact match
    if domain in custom_domains:
        return custom_domains[domain]

    # Wildcard match (e.g., *.example.com)
    for key, ip in custom_domains.items():
        if key.startswith("*.") and domain.endswith(key[2:]):
            return ip

    return None

def list_custom_domains():
    """
    List all custom domain mappings.

    Returns:
        dict: The dictionary of custom domains and their mappings.
    """
    return custom_domains

def save_custom_domains_to_file(file_path):
    """
    Save custom domain mappings to a JSON file.

    Args:
        file_path (str): Path to the file where mappings will be saved.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(custom_domains, file)
        print(f"Custom domains saved to {file_path}.")
    except Exception as e:
        print(f"Error saving custom domains to file: {e}")

def load_custom_domains_from_file(file_path):
    """
    Load custom domain mappings from a JSON file.

    Args:
        file_path (str): Path to the file from which mappings will be loaded.
    """
    global custom_domains
    try:
        with open(file_path, "r") as file:
            custom_domains = json.load(file)
        print(f"Custom domains loaded from {file_path}.")
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with an empty custom domains list.")
    except Exception as e:
        print(f"Error loading custom domains from file: {e}")
