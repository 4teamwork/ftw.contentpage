from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from unittest2 import TestCase


class TestContentPageCreation(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestContentPageCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

    def test_fti(self):
        self.assertIn('ContentPage', self.portal.portal_types.objectIds())

    
