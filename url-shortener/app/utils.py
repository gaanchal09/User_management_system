import random
import string
import re

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_url(url):
    # Simple regex for HTTP/HTTPS URLs
    pattern = r"^(https?://)[\w.-]+(?:\.[\w\.-]+)+(?:[/\w\._~:/?#[\]@!$&'()*+,;=\-]*)?$"
    return re.match(pattern, url) is not None
