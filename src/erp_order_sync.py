import json
from dataclasses import dataclass
from logging import getLogger, INFO
from typing import Dict

logger = getLogger(__name__)
logger.setLevel(INFO)

@dataclass
class ConnectionError:
    error_message: str
    error_details: Dict[str, str]

class ERPOrderSync:
    def __init__(self):
        self.errors = []

    def send_notification(self, error: ConnectionError):
        notification = {
            "error_message": error.error_message,
            "error_details": error.error_details
        }
        logger.info(f"Sending notification: {json.dumps(notification)}")

    def log_error(self, error: ConnectionError):
        self.errors.append(error)
        logger.error(f"Logged error: {error.error_message}")

    def handle_connection_error(self, error_message: str, error_details: Dict[str, str]):
        error = ConnectionError(error_message, error_details)
        self.send_notification(error)
        self.log_error(error)

    def get_logged_errors(self):
        return self.errors
