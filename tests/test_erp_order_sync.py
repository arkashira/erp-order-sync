import pytest
from erp_order_sync import ERPOrderSync, ConnectionError
import logging
from unittest.mock import patch

@pytest.fixture
def erp_order_sync():
    return ERPOrderSync()

def test_send_notification(erp_order_sync, caplog):
    error = ConnectionError("Test error", {"detail": "Test detail"})
    erp_order_sync.send_notification(error)
    assert "Sending notification" in caplog.text

def test_log_error(erp_order_sync, caplog):
    error = ConnectionError("Test error", {"detail": "Test detail"})
    erp_order_sync.log_error(error)
    assert "Logged error" in caplog.text

def test_handle_connection_error(erp_order_sync, caplog):
    error_message = "Test error"
    error_details = {"detail": "Test detail"}
    erp_order_sync.handle_connection_error(error_message, error_details)
    assert "Sending notification" in caplog.text
    assert "Logged error" in caplog.text

def test_get_logged_errors(erp_order_sync):
    error_message = "Test error"
    error_details = {"detail": "Test detail"}
    erp_order_sync.handle_connection_error(error_message, error_details)
    logged_errors = erp_order_sync.get_logged_errors()
    assert len(logged_errors) == 1
    assert logged_errors[0].error_message == error_message
    assert logged_errors[0].error_details == error_details
