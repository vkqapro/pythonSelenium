import pytest
import logging as log
import allure_pytest


@pytest.mark.health
def test_health():
    log.info('Hello World')