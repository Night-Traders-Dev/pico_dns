import struct

def parse_dns_query(data):
    transaction_id = struct.unpack("!H", data[:2])[0]
    flags = struct.unpack("!H", data[2:4])[0]
    question_count = struct.unpack("!H", data[4:6])[0]

    offset = 12
    domain = []
    while data[offset] != 0:
        length = data[offset]
        offset += 1
        domain.append(data[offset:offset + length].decode())
        offset += length
    domain = ".".join(domain)
    qtype, qclass = struct.unpack("!HH", data[offset + 1:offset + 5])

    return {
        "transaction_id": transaction_id,
        "questions": question_count,
        "domain": domain,
        "type": qtype,
        "class": qclass
    }

def create_dns_response(query, ip_address):
    transaction_id = struct.pack("!H", query["transaction_id"])
    flags = struct.pack("!H", 0x8180)  # Standard response, no error
    qdcount = struct.pack("!H", 1)
    ancount = struct.pack("!H", 1)
    nscount = arcount = struct.pack("!H", 0)

    question = query["domain"].split(".")
    question_section = b"".join(len(part).to_bytes(1, "big") + part.encode() for part in question) + b"\x00"
    question_section += struct.pack("!HH", query["type"], query["class"])

    answer_name = b"\xc0\x0c"
    answer_type = struct.pack("!H", 1)
    answer_class = struct.pack("!H", 1)
    ttl = struct.pack("!I", 300)
    rdlength = struct.pack("!H", 4)
    rdata = struct.pack("!BBBB", *[int(octet) for octet in ip_address.split(".")])
    answer_section = answer_name + answer_type + answer_class + ttl + rdlength + rdata

    return transaction_id + flags + qdcount + ancount + nscount + arcount + question_section + answer_section
