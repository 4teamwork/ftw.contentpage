from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from pyquery import PyQuery
from unittest2 import TestCase
from ftw.contentpage.interfaces import ITeaser
import transaction


class TestTeaserImage(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTeaserImage, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()
        self.catalog = getToolByName(self.portal, 'portal_catalog')

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

        # Regular old simplayout page
        self.page = self.portal.get(
            self.portal.invokeFactory('Page', 'page'))
        self.page.processForm()

        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_teaser_interface(self):
        self.assertTrue(ITeaser.providedBy(self.contentpage),
            'ContentPage should provide ITeaser interface')

        self.assertFalse(ITeaser.providedBy(self.page),
            'Old Page should not provide ITeaser interface')



