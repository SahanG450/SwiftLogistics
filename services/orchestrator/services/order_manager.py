"""Order management utilities."""

from datetime import datetime
import random
import string


def create_order_id() -> str:
    """Generate a unique order ID."""
    timestamp = int(datetime.utcnow().timestamp())
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"ORD-{timestamp}-{random_suffix}"
