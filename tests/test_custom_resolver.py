from lib.src.custom_resolver import (
    add_custom_domain,
    remove_custom_domain,
    resolve_custom_domain,
    list_custom_domains,
    save_custom_domains_to_file,
    load_custom_domains_from_file,
)

def test_custom_resolver():
    # Prepare a temporary file
    test_file = "test_custom_domains.json"

    # Test adding custom domains
    add_custom_domain("example.com", "192.168.1.100")
    add_custom_domain("*.example.com", "192.168.1.200")
    assert resolve_custom_domain("example.com") == "192.168.1.100"
    assert resolve_custom_domain("sub.example.com") == "192.168.1.200"
    assert resolve_custom_domain("nonexistent.com") is None

    # Test listing custom domains
    domains = list_custom_domains()
    assert "example.com" in domains
    assert "*.example.com" in domains

    # Test saving and loading custom domains
    save_custom_domains_to_file(test_file)
    remove_custom_domain("example.com")
    load_custom_domains_from_file(test_file)
    assert resolve_custom_domain("example.com") == "192.168.1.100"

    print("Custom resolver tests passed.")

if __name__ == "__main__":
    test_custom_resolver()
