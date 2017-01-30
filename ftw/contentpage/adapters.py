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
        return api.content.create(container=self.context,
                                  type=self.getEventType(),
                                  title=title,
                                  startDate=start_date,
                                  endDate=start_date)
