from src.css_locators.css_locators import SccLocators

import pytest
class BaseTest:
    """

    Class for setting up the base test fixture.

    Attributes:
        SCC: SccLocators

    Methods:
        setup(self, request) - Fixture to set up SccLocators instance for each test.

    """
    SCC: SccLocators
    @pytest.fixture(autouse=True)
    def setup(self, request):
        request.cls.SCC = SccLocators()
