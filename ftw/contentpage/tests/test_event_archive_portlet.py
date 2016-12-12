from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestEventArchivePortlet(FunctionalTestCase):

    def setUp(self):
        super(TestEventArchivePortlet, self).setUp()
        self.grant('Manager')

    @browsing
    def test_event_archive_portlet(self, browser):
        event_folder = create(Builder('event folder'))

        create(Builder('event page')
               .within(event_folder)
               .having(startDate=DateTime(2013, 3, 20, 10, 0))
               .having(endDate=DateTime(2013, 3, 20, 11, 0)))

        create(Builder('event page')
               .within(event_folder)
               .having(startDate=DateTime(2013, 5, 26, 10, 0))
               .having(endDate=DateTime(2013, 5, 26, 11, 0)))

        create(Builder('event page')
               .within(event_folder)
               .having(startDate=DateTime(2013, 6, 28, 10, 0))
               .having(endDate=DateTime(2013, 6, 28, 11, 0)))

        create(Builder('event archive portlet').within(event_folder))

        browser.login().visit(event_folder)

        self.assertTrue(
            browser.css('.portlet.portletArchiveListing'),
            msg='There should be an event archive portlet, but it isn\'t.'
        )

        self.assertEqual(
            3,
            len(browser.css('.portlet.portletArchiveListing .portletItem li.month')),
            msg='There should be 3 entries in the event archive portlet.'
        )

    @browsing
    def test_event_archive_portlet_renders_default_title(self, browser):
        event_folder = create(Builder('event folder'))

        create(Builder('event page')
               .within(event_folder)
               .having(startDate=DateTime(2014, 2, 2))
               .having(endDate=DateTime(2014, 2, 6)))

        create(Builder('event archive portlet').within(event_folder))

        browser.login().visit(event_folder)
        self.assertEqual(
            ['Events'],
            browser.css('dl.portletArchiveListing dt').text
        )

    @browsing
    def test_event_archive_portlet_renders_custom_title(self, browser):
        event_folder = create(Builder('event folder'))

        create(Builder('event page')
               .within(event_folder)
               .having(startDate=DateTime(2014, 2, 2))
               .having(endDate=DateTime(2014, 2, 6)))

        create(Builder('event archive portlet').within(event_folder))
        browser.login()

        # Make sure the portlet renders the default title.
        browser.visit(event_folder)
        self.assertEqual(
            ['Events'],
            browser.css('dl.portletArchiveListing dt').text
        )

        # Now let's change the title of the portlet.
        browser.visit(event_folder, view='@@manage-portlets')
        browser.find('Event Archive Portlet').click()
        browser.fill({'Title': u'Foobar'}).submit()

        # Make sure the portlet renders the custom title.
        browser.visit(event_folder)
        self.assertEqual(
            ['Foobar'],
            browser.css('dl.portletArchiveListing dt').text
        )
