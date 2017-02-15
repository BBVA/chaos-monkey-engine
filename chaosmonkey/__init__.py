"""
Chaos Monkey Engine main package
"""

# Configure default logging for entire app
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s'
)

# different log level for apscheduler to avoid debug flood
logging.getLogger("apscheduler.scheduler").setLevel(logging.INFO)
