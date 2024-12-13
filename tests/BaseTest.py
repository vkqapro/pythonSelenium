from src.locators.locators import Locators

import pytest
class BaseTest:
    """

    Class for setting up the base test fixture.

    Attributes:
        SCC: SccLocators

    Methods:
        setup(self, request) - Fixture to set up SccLocators instance for each test.

    """
    SCC: Locators
    @pytest.fixture(autouse=True)
    def setup(self, request):
        request.cls.SCC = Locators()
