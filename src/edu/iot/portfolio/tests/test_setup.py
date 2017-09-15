# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from edu.iot.portfolio.testing import EDU_IOT_PORTFOLIO_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that edu.iot.portfolio is properly installed."""

    layer = EDU_IOT_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if edu.iot.portfolio is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'edu.iot.portfolio'))

    def test_browserlayer(self):
        """Test that IEduIotPortfolioLayer is registered."""
        from edu.iot.portfolio.interfaces import (
            IEduIotPortfolioLayer)
        from plone.browserlayer import utils
        self.assertIn(IEduIotPortfolioLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EDU_IOT_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['edu.iot.portfolio'])

    def test_product_uninstalled(self):
        """Test if edu.iot.portfolio is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'edu.iot.portfolio'))

    def test_browserlayer_removed(self):
        """Test that IEduIotPortfolioLayer is removed."""
        from edu.iot.portfolio.interfaces import \
            IEduIotPortfolioLayer
        from plone.browserlayer import utils
        self.assertNotIn(IEduIotPortfolioLayer, utils.registered_layers())
