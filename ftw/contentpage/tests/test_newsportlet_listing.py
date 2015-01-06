from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from unittest2 import TestCase

from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING


class TestNewsPortletListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.portal.REQUEST
        self.portal_url = self.portal.portal_url()

    def test_no_portlet_found(self):
        self.request.form.update({'portlet': 'not_existing'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(None, view.get_portlet())

    def test_portlet_found_in_leftcolumn(self):
        portlet = create(Builder('news portlet'))
        self.request.form.update({'portlet': portlet.__name__,
                                  'manager': u'plone.leftcolumn'})
        view = self.portal.unrestrictedTraverse('news_portlet_listing')
        self.assertEqual(portlet,
                         view.get_portlet().data)

    @browsing
    def test_leftcolumn_portlet(self, browser):
        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .having(only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().open()
        browser.find('More News').click()
        self.assertEquals(['Bookings open'],
                          browser.css('h2.tileHeadline').text)

    @browsing
    def test_rightcolumn_portlet(self, browser):
        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .having(only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().open()
        browser.find('More News').click()
        self.assertEquals(['Bookings open'],
                          browser.css('h2.tileHeadline').text)

    @browsing
    def test_newslisting_of_inherited_news_portlet(self, browser):
        # Create a news portlet on root which will be inherited by the root's
        # child objects.
        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .within(self.portal)
               .having(portlet_title='Aktuell',
                       more_news_link=True,
                       quantity=5,
                       days=10))

        # Create a content page having a news folder. Create an old news
        # entry in the news folder.
        content_page = create(Builder('content page')
                              .titled('My Content Page'))
        news_folder = create(Builder('news folder')
                             .titled('News')
                             .within(content_page))
        create(Builder('news')
               .titled('Bookings open')
               .having(effectiveDate=DateTime(1999, 11, 15))
               .within(news_folder))

        # Visit the content page containing the news portlet. The old news
        # entry will not be rendered in the portlet due to the config of the
        # news portlet.
        browser.login().visit(content_page)

        # Clicking on the 'More News' link should render a page containing
        # the news entry.
        browser.find('More News').click()
        self.assertEquals(['Bookings open'],
                          browser.css('h2.tileHeadline').text)
