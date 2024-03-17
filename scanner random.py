
import base58
from bitcoin import *
from tqdm import tqdm
import hashlib
import random

def generate_private_keys(start, end, addresses):
    private_keys = []
    public_keys = []
    
    with tqdm(total=len(addresses), desc="Generating Keys") as pbar:
        while True:
            private_key_int = random.randint(start, end)
            print("Generated private key int:", private_key_int)
            private_key_hex = hex(private_key_int)[2:].zfill(64) + "01"
            print("Generated private key hex:", private_key_hex)
            private_key = base58.b58encode_check(b'\x80' + bytes.fromhex(private_key_hex)).decode('utf-8')

            public_key = privtopub(private_key)
            address = pubtoaddr(public_key)

            if address in addresses:
                private_keys.append(private_key)
                public_keys.append(public_key)
                save_wallet(address, private_key, public_key)  # Save the wallet immediately
                pbar.update(1)  # Increment progress bar
                break  # Stop the loop after finding the corresponding address

    return private_keys, public_keys

def save_wallet(address, private_key, public_key):
    with open(f"{address}_wallet.txt", "w") as file:
        file.write(f"Address: {address}\n")
        file.write(f"Private Key: {private_key}\n")
        file.write(f"Public Key: {public_key}\n")

addresses = [
    "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
]

start = 0x20000000000000000
end = 0x3ffffffffffffffff

private_keys, public_keys = generate_private_keys(start, end, addresses)

# Print the results
for private_key, public_key, address in zip(private_keys, public_keys, addresses):
    print(f"Generated key for address: {address}")
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")
    print()
