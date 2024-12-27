from lib.src.dns_parser import parse_dns_query, create_dns_response, create_error_response

def test_dns_parser():
    # Test parsing a DNS query
    raw_query = b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01'
    query = parse_dns_query(raw_query)
    assert query["transaction_id"] == 0x1234
    assert query["domain"] == "example.com"
    assert query["type"] == 1  # A record
    assert query["class"] == 1  # IN class

    # Test creating a DNS response
    ip_address = "192.168.1.1"
    response = create_dns_response(query, ip_address)
    assert response is not None
    assert len(response) > 0

    # Test creating an error response
    error_response = create_error_response(query)
    assert error_response is not None
    assert len(error_response) > 0

    print("DNS parser tests passed.")

if __name__ == "__main__":
    test_dns_parser()
