"""Message queue service instance."""

import sys
sys.path.append('/app')
from common.messaging import MessageQueue

# Create singleton instance
message_queue = MessageQueue()
