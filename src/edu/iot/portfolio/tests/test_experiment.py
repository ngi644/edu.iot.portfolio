# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from edu.iot.portfolio.interfaces import IExperiment
from edu.iot.portfolio.testing import EDU_IOT_PORTFOLIO_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ExperimentIntegrationTest(unittest.TestCase):

    layer = EDU_IOT_PORTFOLIO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Experiment')
        schema = fti.lookupSchema()
        self.assertEqual(IExperiment, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Experiment')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Experiment')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IExperiment.providedBy(obj))

    def test_adding(self):
        obj = api.content.create(
            container=self.portal,
            type='Experiment',
            id='Experiment',
        )
        self.assertTrue(IExperiment.providedBy(obj))
