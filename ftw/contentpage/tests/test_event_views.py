from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.contentpage.browser.eventlisting import EventListing
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from ftw.testing import MockTestCase
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from Products.Five.browser import BrowserView
from pyquery import PyQuery
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager
import os
import transaction


class TestEventListingIntegration(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.folder = create(Builder('event folder'))

    def test_pending_events_are_still_visible(self):
        event = create(Builder('event page').within(self.folder).having(
            startDate=DateTime()-1,
            endDate=DateTime()+1)
        )

        view = EventListing(self.folder, self.request)

        self.assertEqual(
            [event],
            [brain.getObject() for brain in view.get_items()])

    def test_month_year_filter_on_eventlisting(self):
        event = create(Builder('event page').within(self.folder).having(
            startDate=DateTime('2014/02/02'),
            endDate=DateTime('2014/02/06'))
        )
        view = EventListing(self.folder, self.request)

        self.assertEquals(0, len(view.get_items()))
        self.request.set('archive', '2014/02/01')

        self.assertEquals(1, len(view.get_items()))


class TestEventListing(MockTestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestEventListing, self).setUp()
        self.mock_current_time(2013, 05, 20, 10, 00)

        from DateTime import DateTime

        self.portal = self.layer['portal']
        self.eventfolder = self.portal.get(
        self.portal.invokeFactory('EventFolder', 'eventfolder'))
        self.eventfolder.invokeFactory('EventPage', 'event1', title="Event1",
                                       startDate=DateTime(
                                           2013, 03, 20, 10, 00),
                                       endDate=DateTime(2013, 03, 20, 11, 00),
                                       )
        self.eventfolder.invokeFactory('EventPage', 'event2', title="Event2",
                                       startDate=DateTime(
                                           2013, 05, 22, 10, 00),
                                       endDate=DateTime(2013, 05, 22, 11, 00),
                                       location="Bern")
        file_ = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        self.eventfolder.invokeFactory('EventPage', 'event3', title="Event3",
                                       startDate=DateTime(
                                           2013, 05, 24, 10, 00),
                                       endDate=DateTime(2013, 05, 24, 11, 00),
                                       location="Berns",
                                       image=file_)

        self.eventfolder.invokeFactory('EventPage', 'event4', title="Event4",
                                       startDate=DateTime(
                                           2013, 05, 26, 10, 00),
                                       endDate=DateTime(2013, 05, 26, 11, 00),
                                       location="Bern")

        self.eventfolder.invokeFactory('EventPage', 'event5', title="Event5",
                                       startDate=DateTime(
                                           2013, 06, 28, 10, 00),
                                       endDate=DateTime(2013, 06, 28, 11, 00),
                                       location="Bern")

        self.eventfolder.invokeFactory('EventPage', 'event6', title="Event6",
                                       startDate=DateTime(
                                           2013, 05, 30, 10, 00),
                                       endDate=DateTime(2013, 05, 30, 11, 00),
                                       location="Bern")

        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def mock_current_time(self, *dtargs):
        # since mocker is not able to replace (a.k.a monkeypatch)
        # datetime.datetime.now directly, we need to make a proxy
        # of the datetime class and mix it in by replacing the
        # datetime module...
        from datetime import datetime, timedelta
        pydt_now = datetime(*dtargs)
        pydt_class = self.mocker.proxy(datetime)
        self.expect(pydt_class.now()).result(pydt_now).count(0, None)
        pydt_mod = self.mocker.replace('datetime')
        self.expect(pydt_mod.datetime).result(pydt_class).count(0, None)
        self.expect(pydt_mod.timedelta).result(timedelta).count(0, None)

        from DateTime import DateTime
        zdt_now = DateTime(pydt_now)
        zdt_mod = self.mocker.replace('DateTime')
        self.expect(zdt_mod.DateTime()).result(zdt_now).count(0, None)

        self.mocker.replay()

    def test_listing_no_past_events(self):
        view = self.eventfolder.restrictedTraverse('event_listing')
        events = view.get_items()
        self.assertEqual(len(events), 5)

    def test_listing_sort(self):
        view = self.eventfolder.restrictedTraverse('event_listing')
        events = view.get_items()
        for index, event in enumerate(events):
            if not index == len(events) - 1:
                self.assertTrue(event.start < events[index + 1].start)

    def test_listing_archive(self):
        view = self.eventfolder.restrictedTraverse('event_listing')
        self.portal.REQUEST['archive'] = '2013/06/01'
        events = view.get_items()
        self.assertEqual(len(events), 1)

        from DateTime import DateTime
        self.assertEqual(events[0].start, DateTime(2013, 06, 28, 10, 00))

    def test_has_img(self):
        view = self.eventfolder.restrictedTraverse('event_listing')
        events = view.get_items()
        self.assertFalse(view.has_img(events[0]))
        self.assertTrue(view.has_img(events[1]))

    def test_browser(self):
        self.browser.open(self.eventfolder.absolute_url())
        query = PyQuery(self.browser.contents)
        element = query('.tileImage')
        self.assertEqual(element.attr('alt'), 'Event3')
        self.assertEqual(element.attr('title'), 'Event3')
        self.assertEqual(element.attr('width'), '100')

    @browsing
    def test_whole_day_event(self, browser):
        self.eventfolder.invokeFactory('EventPage', 'event7', title="Event7",
                                       wholeDay=True,
                                       startDate=DateTime(2013, 05, 20, 4, 0),
                                       endDate=DateTime(2013, 05, 20, 5, 0),
                                       location="Bern")
        transaction.commit()
        browser.visit(self.eventfolder)
        event_heading_links = browser.css('.tileHeadline').css('.url')
        event_titles = [link.text for link in event_heading_links]
        self.assertIn('Event7', event_titles)

    def test_event_view(self):
        event1 = self.eventfolder.get('event1')
        event2 = self.eventfolder.get('event2')
        self.browser.open(event1.absolute_url())
        query = PyQuery(self.browser.contents)
        elements = query('.eventdata tr th')
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0].text.strip(), 'Date')
        self.assertEqual(elements[1].text.strip(), 'Export')

        self.browser.open(event2.absolute_url())
        query = PyQuery(self.browser.contents)
        elements = query('.eventdata tr th')
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].text.strip(), 'Date')
        self.assertEqual(elements[1].text.strip(), 'Location')
        self.assertEqual(elements[2].text.strip(), 'Export')
        location = query('.eventdata tr td')[-2]
        self.assertEqual(location.text, event2.getLocation())

    def test_event_data_viewlet(self):
        event = self.eventfolder.get('event3')  # has an image
        view = BrowserView(event, event.REQUEST)
        manager_name = 'plone.abovecontentbody'
        manager = queryMultiAdapter((event, event.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)
        # Set up viewlets
        manager.update()
        name = 'ftw.contentpage.event.eventdata'
        viewlet = [v for v in manager.viewlets if v.__name__ == name][0]

        self.failUnless(viewlet)
