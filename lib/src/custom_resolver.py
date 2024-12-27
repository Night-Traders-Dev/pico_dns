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
    Resolve a domain using custom mappings.

    Args:
        domain (str): The domain name.

    Returns:
        str: The resolved IP address or None if not found.
    """
    return custom_domains.get(domain)
