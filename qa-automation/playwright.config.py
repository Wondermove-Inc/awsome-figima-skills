import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "multi_account: mark test as requiring multiple browser accounts"
    )
