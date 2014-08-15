from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from unittest2 import TestCase
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings.interfaces import IGeoFeatureStyle
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.interfaces import IPortletManager


class TestAddressGeoConfigHandler(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestAddressGeoConfigHandler, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

    def test_setuphandler_called_again(self):
        setup = getToolByName(self.portal, 'portal_setup')
        setup.runAllImportStepsFromProfile(
            'profile-ftw.contentpage:default',
            ignore_dependencies=True,
            purge_old=False)

        # Check geo settings
        registry = getUtility(IRegistry)
        geo_content_types = registry.forInterface(
            IGeoSettings).geo_content_types
        self.assertIn('AddressBlock', geo_content_types)

        map_viewlet_position = registry.forInterface(
            IGeoFeatureStyle).map_viewlet_position
        self.assertEquals(map_viewlet_position, 'fake-manager')

        # Check dropzone portlet - There should only be one
        manager = getUtility(IPortletManager, name=u"plone.rightcolumn")
        mapping = manager[CONTENT_TYPE_CATEGORY][u"ContentPage"]
        self.assertEquals(len(mapping), 1)
