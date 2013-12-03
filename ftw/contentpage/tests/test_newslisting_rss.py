import transaction

from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from unittest2 import TestCase


class TestNewsRssListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('NewsFolder', 'nf1')
        self.context = self.portal.nf1
        self.context.invokeFactory('News', 'n1')
        transaction.commit()

    def login(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_newslisting_rss_items(self):
        self.browser.open(self.context.absolute_url() + '/news_rss_listing')
        self.assertIn('<rdf:li rdf:resource="http://nohost/plone/nf1/n1"/>',self.browser.contents)
        self.assertIn('<link>http://nohost/plone/nf1/n1</link>', self.browser.contents)
