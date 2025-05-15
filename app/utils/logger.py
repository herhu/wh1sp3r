"""
Global logging utility adapted for AWS Lambda
"""

import logging

# Configure logging only once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()  # Lambda logs van a CloudWatch automáticamente
    ]
)

def get_logger(name: str):
    return logging.getLogger(name)
