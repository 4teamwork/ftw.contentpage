from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from unittest2 import TestCase


class TestMarkerInterfaceForListings(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestMarkerInterfaceForListings, self).setUp()

        self.portal = self.layer['portal']

    def test_contentpage_is_extended_with_checkbox(self):
        page = create(Builder('content page'))

        fieldname = 'mark_for_listings'
        self.assertIn(fieldname,
                      page.Schema().keys(),
                      '{0} nod found in content page schema'.format(fieldname))
