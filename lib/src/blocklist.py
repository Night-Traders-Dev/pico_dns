import json

blocklist = set()

def load_blocklist(file_path):
    """
    Load the blocklist from a file.

    Args:
        file_path (str): Path to the blocklist file.
    """
    global blocklist
    try:
        with open(file_path, "r") as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith("#"):
                    blocklist.add(domain)
        print(f"Blocklist loaded with {len(blocklist)} entries.")
    except FileNotFoundError:
        print(f"Blocklist file {file_path} not found. Starting with an empty blocklist.")
    except Exception as e:
        print(f"Error loading blocklist: {e}")

def save_blocklist(file_path):
    """
    Save the blocklist to a file.

    Args:
        file_path (str): Path to the blocklist file.
    """
    try:
        with open(file_path, "w") as f:
            for domain in blocklist:
                f.write(domain + "\n")
        print(f"Blocklist saved to {file_path}.")
    except Exception as e:
        print(f"Error saving blocklist: {e}")

def add_to_blocklist(domain):
    """
    Add a domain to the blocklist.

    Args:
        domain (str): Domain to block.
    """
    if domain not in blocklist:
        blocklist.add(domain)
        print(f"Added {domain} to blocklist.")
    else:
        print(f"{domain} is already in the blocklist.")

def remove_from_blocklist(domain):
    """
    Remove a domain from the blocklist.

    Args:
        domain (str): Domain to unblock.
    """
    if domain in blocklist:
        blocklist.remove(domain)
        print(f"Removed {domain} from blocklist.")
    else:
        print(f"{domain} not found in blocklist.")

def is_blocked(domain):
    """
    Check if a domain is blocked, including wildcard matching.

    Args:
        domain (str): The domain to check.

    Returns:
        bool: True if the domain is blocked, False otherwise.
    """
    # Exact match
    if domain in blocklist:
        return True

    # Wildcard match (e.g., *.example.com)
    for blocked_domain in blocklist:
        if blocked_domain.startswith("*.") and domain.endswith(blocked_domain[2:]):
            return True

    return False

def list_blocked_domains():
    """
    List all domains in the blocklist.

    Returns:
        set: The set of blocked domains.
    """
    return blocklist
