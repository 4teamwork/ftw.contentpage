from ftw.builder import Builder
from ftw.builder import create
from ftw.calendar.browser.interfaces import IFtwCalendarEventCreator
from ftw.contentpage.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from zope.component import getMultiAdapter
from DateTime import DateTime


class TestEventCreatorAdapter(FunctionalTestCase):

    def setUp(self):
        super(TestEventCreatorAdapter, self).setUp()
        self.grant('Manager')

    def test_event_creator_adapter_type(self):

        eventCreator = getMultiAdapter((self.portal, self.request),
                                       IFtwCalendarEventCreator)

        self.assertEqual("EventPage", eventCreator.getEventType())

    @browsing
    def test_event_creator_adapter(self, browser):
        event_folder = create(Builder('event folder'))

        eventCreator = getMultiAdapter((event_folder, self.request),
                                       IFtwCalendarEventCreator)

        now = DateTime()

        event = eventCreator.createEvent("test", now)

        self.assertEqual('test', event.Title())
        self.assertEqual(now, event.start())


