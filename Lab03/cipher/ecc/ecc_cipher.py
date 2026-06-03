import ecdsa
import os

# Ensure the directory exists
if not os.path.exists('cipher/ecc/keys'):
    os.makedirs('cipher/ecc/keys')

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        # Generate ECC signing and verifying keys
        sk = ecdsa.SigningKey.generate()  # Private key
        vk = sk.get_verifying_key()       # Public key

        # Write private key to file
        with open('cipher/ecc/keys/privateKey.pem', 'wb') as p:
            p.write(sk.to_pem())

        # Write public key to file
        with open('cipher/ecc/keys/publicKey.pem', 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        # Load private and public keys from files
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk

    def sign(self, message, key):
        """Signs a message with the provided private key."""
        return key.sign(message.encode('ascii'))

    def verify(self, message, signature, key=None):
        """Verifies a message using the public key."""
        if key is None:
            _, vk = self.load_keys()  # Load the public key from file if not provided
        else:
            vk = key

        try:
            # Verify the signature
            return vk.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            # If the signature is invalid, return False
            return False
