from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from unittest2 import TestCase
import transaction


class TestNewsRssListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.newsfolder = create(Builder('news folder')
                                 .titled('Ein N\xc3\xbcwsFolder'))
        self.news = create(Builder('news').within(self.newsfolder))

        transaction.commit()

    def login(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

    def test_newslisting_rss_items(self):
        self.browser.open(self.newsfolder.absolute_url() + '/news_rss_listing')

        title = '<title>{}</title>'.format(self.news.title)
        self.assertIn(title,
                      self.browser.contents,
                      'Could not find the title of the news')

        link = '<link>{}</link>'.format(self.news.absolute_url())
        self.assertIn(link,
                      self.browser.contents,
                      'Could not find the link tag for the news')

    @browsing
    def test_newsitem_contains_pubdate(self, browser):
        browser.open(self.newsfolder, view='news_rss_listing')
        browser.parse_as_html()  # use HTML parser so that we have no XML namespaces.

        effective_date = self.news.effective()
        self.assertEqual(
            # Since w3c suggests using rfc822 for pubDate, we can simply
            # use the already implemented method for this.
            effective_date.rfc822(),
            browser.css('rss item pubDate').first.text
        )
