from DateTime import DateTime
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from plone.testing.z2 import Browser
import transaction
import unittest2 as unittest


class TestEvent(unittest.TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.eventfolder = self.portal.get(
            self.portal.invokeFactory('EventFolder', 'eventfolder'))
        self.event = self.eventfolder.get(
            self.eventfolder.invokeFactory('EventPage', 'event'))
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def test_event_date_single_day(self):
        self.event.startDate = DateTime(2013, 05, 30, 18, 00)
        self.event.endDate = DateTime(2013, 05, 30, 19, 00)
        date = self.event.getDate()
        self.assertEqual(date, '30.05.2013 18:00 - 19:00')

    def test_event_date_multiple_day(self):
        self.event.startDate = DateTime(2013, 05, 30, 18, 00)
        self.event.endDate = DateTime(2013, 05, 31, 19, 00)
        date = self.event.getDate()
        self.assertEqual(date, '30.05.2013 18:00 - 31.05.2013 19:00')

    def test_event_date_whole_day(self):
        self.event.startDate = DateTime(2013, 05, 30, 18, 00)
        self.event.endDate = DateTime(2013, 05, 30, 19, 00)
        self.event.wholeDay = True
        date = self.event.getDate()
        self.assertEqual(date, '30.05.2013')