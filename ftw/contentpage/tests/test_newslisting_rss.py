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

        rdf = '<rdf:li rdf:resource="{0}"/>'.format(
            self.news.absolute_url())
        self.assertIn(rdf,
                      self.browser.contents,
                      'Did not found the rdf tag for the news')

        link = '<link>{0}</link>'.format(self.news.absolute_url())
        self.assertIn(link,
                      self.browser.contents,
                      'Did not found the link tag for the news')

    @browsing
    def test_newsitem_contains_pubdate(self, browser):
        browser.open(self.newsfolder, view='news_rss_listing')
        browser.parse_as_html()  # use HTML parser so that we have no XML namespaces.

        effective_date = self.news.getEffectiveDate()
        self.assertEqual(
            # Difference between "%e" and "%-e":
            # %e has a leading space on single numbers - thats why the tests
            # failing between the 1st and the 9th every month :-)
            # %-e Removes the leading space - only works on unix machines.
            effective_date.strftime('%a, %-e %b %Y %H:%M:%S %z').strip(),
            browser.css('rdf item pubDate').first.text
        )
