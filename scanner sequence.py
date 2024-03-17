import base58
from bitcoin import *
import hashlib
from tqdm import tqdm

def generate_private_keys(start, end, addresses):
    private_keys = []
    public_keys = []

    with tqdm(total=end-start) as pbar:
        for i in range(start, end):
            private_key_hex = hex(i)[2:].zfill(64) + "01"
            private_key = base58.b58encode_check(b'\x80' + bytes.fromhex(private_key_hex)).decode('utf-8')

            public_key = privtopub(private_key)
            address = pubtoaddr(public_key)

            if address in addresses:
                private_keys.append(private_key)
                public_keys.append(public_key)
                save_to_file(private_keys, public_keys)
                break

            pbar.update(1)

    return private_keys, public_keys

def save_to_file(private_keys, public_keys):
    with open("private_keys_public_keys.txt", "w") as file:
        for private_key, public_key in zip(private_keys, public_keys):
            file.write(f"Private Key: {private_key}\nPublic Key: {public_key}\n\n")

addresses = [
    "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
    # Rest of the addresses...
]

start = 0x20000000000000000
end = 0x3ffffffffffffffff

private_keys, public_keys = generate_private_keys(start, end, addresses)

# Print the results
for private_key, public_key in zip(private_keys, public_keys):
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
    print()
