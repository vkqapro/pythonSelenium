from src.css_locators.css_locators import SccLocators

import pytest
class BaseTest:
    SCC: SccLocators
    @pytest.fixture(autouse=True)
    def setup(self, request):
        request.cls.SCC = SccLocators()
