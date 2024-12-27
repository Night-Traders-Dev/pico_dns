blocklist = set()

def load_blocklist(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith("#"):
                    blocklist.add(domain)
        print(f"Blocklist loaded with {len(blocklist)} entries.")
    except FileNotFoundError:
        print("Blocklist file not found. Starting with an empty blocklist.")
    except Exception as e:
        print(f"Error loading blocklist: {e}")

def add_to_blocklist(domain):
    blocklist.add(domain)
    print(f"Added {domain} to blocklist.")

def remove_from_blocklist(domain):
    if domain in blocklist:
        blocklist.remove(domain)
        print(f"Removed {domain} from blocklist.")
    else:
        print(f"{domain} not found in blocklist.")

def is_blocked(domain):
    return domain in blocklist
