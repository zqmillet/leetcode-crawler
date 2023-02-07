from zlib import compress
from zlib import decompress
from base64 import b64encode
from base64 import b64decode

def encode(text: str) -> str:
    compressed_bytes = compress(text.encode('utf8'))
    return b64encode(compressed_bytes).encode('utf8')

def decode(text: str) -> str:
    return decompress(b64decode(text))

