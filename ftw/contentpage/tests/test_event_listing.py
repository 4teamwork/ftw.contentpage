from DateTime import DateTime
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
from pyquery import PyQuery
import os
import transaction
import unittest2 as unittest


class TestEventListing(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.eventfolder = self.portal.get(
          self.portal.invokeFactory('EventFolder', 'eventfolder'))
        self.eventfolder.invokeFactory('EventPage', 'event1', title="Event1",
                                       startDate=DateTime(
                                           2013, 03, 20, 10, 00),
                                       endDate=DateTime(2013, 03, 20, 11, 00),
                                       location="Bern")
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
        self.portal.REQUEST['archiv'] = '2013/06/01'
        events = view.get_items()
        self.assertEqual(len(events), 1)
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
