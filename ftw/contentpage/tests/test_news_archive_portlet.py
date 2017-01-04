from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestNewsArchivePortlet(FunctionalTestCase):

    def setUp(self):
        super(TestNewsArchivePortlet, self).setUp()
        self.grant('Manager')

    @browsing
    def test_news_archive_portlet(self, browser):
        news_folder = create(Builder('news folder'))

        create(Builder('news')
               .within(news_folder)
               .having(effectiveDate=DateTime(2013, 3, 20, 10, 0)))

        create(Builder('news')
               .within(news_folder)
               .having(effectiveDate=DateTime(2013, 5, 26, 10, 0)))

        create(Builder('news')
               .within(news_folder)
               .having(effectiveDate=DateTime(2013, 6, 28, 10, 0)))

        create(Builder('news archive portlet').within(news_folder))

        browser.login().visit(news_folder)

        self.assertTrue(
            browser.css('.portlet.portletArchiveListing'),
            msg='There should be an news archive portlet, but it isn\'t.'
        )

        self.assertEqual(
            3,
            len(browser.css('.portlet.portletArchiveListing .portletItem li.month')),
            msg='There should be 3 entries in the news archive portlet.'
        )

    @browsing
    def test_news_archive_portlet_renders_default_title(self, browser):
        news_folder = create(Builder('news folder'))

        create(Builder('news')
               .within(news_folder)
               .having(effectiveDate=DateTime(2014, 2, 2)))

        create(Builder('news archive portlet').within(news_folder))

        browser.login().visit(news_folder)
        self.assertEqual(
            ['Archive'],
            browser.css('dl.portletArchiveListing dt').text
        )

    @browsing
    def test_news_archive_portlet_renders_custom_title(self, browser):
        news_folder = create(Builder('news folder'))

        create(Builder('news')
               .within(news_folder)
               .having(effectiveDate=DateTime(2014, 2, 2)))

        create(Builder('news archive portlet').within(news_folder))
        browser.login()

        # Make sure the portlet renders the default title.
        browser.visit(news_folder)
        self.assertEqual(
            ['Archive'],
            browser.css('dl.portletArchiveListing dt').text
        )

        # Now let's change the title of the portlet.
        browser.visit(news_folder, view='@@manage-portlets')
        browser.find('News Archive Portlet').click()
        browser.fill({'Title': u'Our Custom Title'}).submit()

        # Make sure the portlet renders the custom title.
        browser.visit(news_folder)
        self.assertEqual(
            ['Our Custom Title'],
            browser.css('dl.portletArchiveListing dt').text
        )
