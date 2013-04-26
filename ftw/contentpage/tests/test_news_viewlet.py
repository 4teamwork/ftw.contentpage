#from DateTime import DateTime
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
import transaction
import unittest2 as unittest


class TestNewsViewlet(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.newsfolder = self.portal.get(
            self.portal.invokeFactory('NewsFolder', 'Newsfolder'))
        self.news = self.newsfolder.get(
            self.newsfolder.invokeFactory('News', 'News1'))
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_event_date_single_day(self):
        self._auth()
        self.browser.open(self.news.absolute_url())
        self.assertIn('<div class="newsPublicationDate">', self.browser.contents)
