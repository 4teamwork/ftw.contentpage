from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.interfaces import IListingMarker
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

    def test_listing_marker_is_set_if_checkbox_is_true(self):
        page = create(Builder('content page'))
        page.Schema()['mark_for_listings'].set(page, True)

        self.assertTrue(IListingMarker.providedBy(page),
                        '{0} is not marked for listings'.format(page))

    def test_listing_marker_is_not_set_if_checkbox_is_false(self):
        page = create(Builder('content page'))
        page.Schema()['mark_for_listings'].set(page, False)

        self.assertFalse(IListingMarker.providedBy(page),
                        '{0} is marked for listings'.format(page))
