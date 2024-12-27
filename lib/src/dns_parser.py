import struct

def parse_dns_query(data):
    """
    Parse a DNS query packet.

    Args:
        data (bytes): Raw DNS query packet.

    Returns:
        dict: Parsed query fields including transaction ID, domain, type, and class.
    """
    try:
        transaction_id = struct.unpack("!H", data[:2])[0]
        flags = struct.unpack("!H", data[2:4])[0]
        question_count = struct.unpack("!H", data[4:6])[0]

        offset = 12
        domain_parts = []
        while data[offset] != 0:
            length = data[offset]
            offset += 1
            domain_parts.append(data[offset:offset + length].decode())
            offset += length
        domain = ".".join(domain_parts)
        qtype, qclass = struct.unpack("!HH", data[offset + 1:offset + 5])

        return {
            "transaction_id": transaction_id,
            "flags": flags,
            "questions": question_count,
            "domain": domain,
            "type": qtype,
            "class": qclass
        }
    except Exception as e:
        print(f"Error parsing DNS query: {e}")
        return None

def create_dns_response(query, ip_address):
    """
    Create a DNS response packet for an A record.

    Args:
        query (dict): Parsed DNS query fields.
        ip_address (str): IP address to map the domain to.

    Returns:
        bytes: DNS response packet.
    """
    try:
        transaction_id = struct.pack("!H", query["transaction_id"])
        flags = struct.pack("!H", 0x8180)  # Standard response, no error
        qdcount = struct.pack("!H", 1)  # Number of questions
        ancount = struct.pack("!H", 1)  # Number of answers
        nscount = arcount = struct.pack("!H", 0)  # No authority or additional records

        # Question section (repeat query)
        question_parts = query["domain"].split(".")
        question_section = b"".join(len(part).to_bytes(1, "big") + part.encode() for part in question_parts) + b"\x00"
        question_section += struct.pack("!HH", query["type"], query["class"])

        # Answer section
        answer_name = b"\xc0\x0c"  # Pointer to the domain name in the question
        answer_type = struct.pack("!H", 1)  # A record
        answer_class = struct.pack("!H", 1)  # IN
        ttl = struct.pack("!I", 300)  # 5-minute TTL
        rdlength = struct.pack("!H", 4)  # IPv4 address length
        rdata = struct.pack("!BBBB", *[int(octet) for octet in ip_address.split(".")])
        answer_section = answer_name + answer_type + answer_class + ttl + rdlength + rdata

        return transaction_id + flags + qdcount + ancount + nscount + arcount + question_section + answer_section
    except Exception as e:
        print(f"Error creating DNS response: {e}")
        return None

def create_error_response(query, error_code=3):
    """
    Create a DNS error response packet.

    Args:
        query (dict): Parsed DNS query fields.
        error_code (int): Error code (default 3: Name Error).

    Returns:
        bytes: DNS error response packet.
    """
    try:
        transaction_id = struct.pack("!H", query["transaction_id"])
        flags = struct.pack("!H", 0x8183)  # Standard response with error
        qdcount = struct.pack("!H", 1)  # Number of questions
        ancount = nscount = arcount = struct.pack("!H", 0)  # No answers, authority, or additional records

        # Question section (repeat query)
        question_parts = query["domain"].split(".")
        question_section = b"".join(len(part).to_bytes(1, "big") + part.encode() for part in question_parts) + b"\x00"
        question_section += struct.pack("!HH", query["type"], query["class"])

        return transaction_id + flags + qdcount + ancount + nscount + arcount + question_section
    except Exception as e:
        print(f"Error creating DNS error response: {e}")
        return None
