from ftw.calendar.browser.interfaces import IFtwCalendarEventCreator
from plone import api
from zope.interface import implements


class CalendarEventPageCreator(object):
    implements(IFtwCalendarEventCreator)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getEventType(self):
        return "EventPage"

    def createEvent(self, title, start_date):
        event = api.content.create(
            container=self.context,
            type=self.getEventType(),
            title=title,
        )

        # Setting the dates does not work via "api.content.create()", reason unknown.
        event.setStartDate(start_date)
        event.setEndDate(start_date)
        event.reindexObject(idxs=['start', 'end'])

        return event
