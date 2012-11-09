from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.component import queryAdapter
from collective.geo.settings.interfaces import IGeoCustomFeatureStyle


class TestAddressGeoConfigHandler(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestAddressGeoConfigHandler, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

    def _create_addressblock(self):
        addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        # Fire all necessary events
        addressblock.processForm()
        addressblock.reindexObject()
        return addressblock

    def test_geo_init_handler(self):
        addressblock = self._create_addressblock()
        adapter = queryAdapter(addressblock, IGeoCustomFeatureStyle)
        self.assertTrue(adapter.use_custom_styles)
        self.assertEquals(adapter.map_viewlet_position, 'fake-manager')

    def tearDown(self):
        super(TestAddressGeoConfigHandler, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
