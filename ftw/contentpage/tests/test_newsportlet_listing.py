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
        view = self.portal.unrestrictedTraverse('newsportlet_listing')
        self.assertEqual(None, view.get_portlet())

    def test_portlet_found_in_leftcolumn(self):
        portlet = create(Builder('news portlet'))
        self.request.form.update({'portlet': portlet.__name__,
                                  'manager': u'plone.leftcolumn'})
        view = self.portal.unrestrictedTraverse('newsportlet_listing')
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

    @browsing
    def test_newslisting_title(self, browser):
        """
        This test makes sure that the news listing view renders the
        title of the portlet, not the generic title.
        """
        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .having(portlet_title='Breaking News',
                       only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().open()
        browser.find('More News').click()
        self.assertEquals(
            ['Breaking News'],
            browser.css('h1.documentFirstHeading').text
        )

    @browsing
    def test_newslisting_no_description(self, browser):
        """
        This test makes sure that the news listing view does not
        render the generic description.
        """
        content_page = create(Builder('content page')
                              .titled('My Page')
                              .having(description='My Description'))

        folder = create(Builder('news folder').titled('News'))
        create(Builder('news').titled('Bookings open').within(folder))

        create(Builder('news portlet')
               .within(content_page)
               .in_manager(u'plone.rightcolumn')
               .having(only_context=False,
                       path=['/{0}'.format(folder.getId())],
                       more_news_link=True))

        browser.login().visit(content_page)
        browser.find('More News').click()
        self.assertEquals(
            0,
            len(browser.css('div.documentDescription'))
        )

    @browsing
    def test_all_news(self, browser):
        """
        This test makes sure that the number of news entries is not limited
        when rendering "all news".
        """

        # Create a news portlet which limits the number of news entries to one.
        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .within(self.portal)
               .having(portlet_title='Aktuell',
                       more_news_link=True,
                       quantity=1))

        # Create a content page having a news folder.
        content_page = create(Builder('content page')
                              .titled('My Content Page'))
        news_folder = create(Builder('news folder')
                             .titled('News')
                             .within(content_page))

        # Create two news entries.
        create(Builder('news').titled('News item 1').within(news_folder))
        create(Builder('news').titled('News item 2').within(news_folder))

        # Visit the content page containing the news portlet.
        browser.login().visit(content_page)

        # Clicking on the 'More News' link should render a page containing
        # both news entries.
        browser.find('More News').click()
        self.assertEquals(
            2,
            len(browser.css('div.newsListing div.tileItem'))
        )

    @browsing
    def test_news_listing_fixes_context_on_news_item(self, browser):
        """
        When news listing is called on a news item it needs to change its
        context for its search starting point. Else it would only display
        the current item.
        """
        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .within(self.portal)
               .having(portlet_title='Aktuell',
                       more_news_link=True,
                       quantity=0))

        # Create a content page having a news folder.
        content_page = create(Builder('content page')
                              .titled('My Content Page'))
        news_folder = create(Builder('news folder')
                             .titled('News')
                             .within(content_page))
        item1 = create(
            Builder('news').titled('News item 1').within(news_folder))
        create(Builder('news').titled('News item 2').within(news_folder))
        create(Builder('news').titled('News item 3').within(news_folder))

        browser.open(item1)
        # check items in news portlet
        self.assertEqual(
            ['News item 1', 'News item 2', 'News item 3'],
            browser.css('.portletWrapper .newsTemplate .portletItem .portletItemTitle').text
        )

        browser.find('More News').click()
        # check news items in news listing view
        self.assertEquals(
            ['News item 1', 'News item 2', 'News item 3'],
            browser.css('.newsListing .tileHeadline a').text
        )

    @browsing
    def test_news_listing_renders_expired_items(self, browser):
        news_folder = create(Builder('news folder'))

        # Create six news items.
        create(Builder('news')
               .titled('Default News')
               .within(news_folder))
        create(Builder('news')
               .titled('Default News With Expiration Date')
               .within(news_folder)
               .having(expirationDate=DateTime() + 20))
        create(Builder('news')
               .titled('Future News')
               .within(news_folder)
               .having(effectiveDate=DateTime() + 10))
        create(Builder('news')
               .titled('Future News With Expiration Date')
               .within(news_folder)
               .having(effectiveDate=DateTime() + 10)
               .having(expirationDate=DateTime() + 20))
        create(Builder('news')
               .titled('Old News')
               .within(news_folder)
               .having(effectiveDate=DateTime() - 10))
        create(Builder('news')
               .titled('Old News (Expired)')
               .within(news_folder)
               .having(effectiveDate=DateTime() - 20)
               .having(expirationDate=DateTime() - 10))

        create(Builder('news portlet')
               .in_manager(u'plone.rightcolumn')
               .within(self.portal)
               .having(portlet_title='My Portlet',
                       more_news_link=True,
                       quantity=100))

        # Make sure the admin sees all news entries, even expired and future
        # news items.
        browser.login().open().find('More News').click()
        self.assertEqual(
            [
                'Future News',
                'Future News With Expiration Date',
                'Default News',
                'Default News With Expiration Date',
                'Old News',
                'Old News (Expired)',
            ],
            browser.css('.newsListing .tileHeadline a').text
        )

        # Make sure the anonymous user only sees news entries which are
        # not expired and not in the future.
        browser.logout().open().find('More News').click()
        self.assertEquals(
            [
                'Default News With Expiration Date',
                'Default News',
                'Old News',
            ],
            browser.css('.newsListing .tileHeadline a').text
        )

        # Configure the portlet to show expired news too.
        browser.login()
        browser.visit(self.portal, view='manage-portlets')
        browser.find('News Portlet (My Portlet)').click()
        browser.fill({u'Show expired items': True}).submit()
        browser.forms['form'].fill({u'Show expired items': True}).find('Save').click()

        # Make sure the admin still sees all news entries, even expired
        # and future news items.
        browser.login().open().find('More News').click()
        self.assertEqual(
            [
                'Future News',
                'Future News With Expiration Date',
                'Default News',
                'Default News With Expiration Date',
                'Old News',
                'Old News (Expired)',
            ],
            browser.css('.newsListing .tileHeadline a').text
        )

        # Make sure the anonymous user sees all news entries, even the
        # expired ones. But not the future news.
        browser.logout().open().find('More News').click()
        self.assertEqual(
            [
                'Default News With Expiration Date',
                'Default News',
                'Old News',
                'Old News (Expired)',
            ],
            browser.css('.newsListing .tileHeadline a').text
        )
