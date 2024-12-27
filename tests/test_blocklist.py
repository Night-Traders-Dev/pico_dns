from lib.src.blocklist import (
    load_blocklist,
    save_blocklist,
    add_to_blocklist,
    remove_from_blocklist,
    is_blocked,
    list_blocked_domains,
)

def test_blocklist():
    # Prepare a temporary blocklist file
    test_file = "test_blocklist.txt"

    # Test adding to blocklist
    add_to_blocklist("ads.google.com")
    add_to_blocklist("*.example.com")
    assert is_blocked("ads.google.com") is True
    assert is_blocked("sub.example.com") is True
    assert is_blocked("nonexistent.com") is False

    # Test listing blocklist
    blocked = list_blocked_domains()
    assert "ads.google.com" in blocked
    assert "*.example.com" in blocked

    # Test saving and loading blocklist
    save_blocklist(test_file)
    remove_from_blocklist("ads.google.com")
    load_blocklist(test_file)
    assert is_blocked("ads.google.com") is True

    print("Blocklist tests passed.")

if __name__ == "__main__":
    test_blocklist()
