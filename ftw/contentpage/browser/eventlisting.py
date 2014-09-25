from ftw.contentpage.browser.baselisting import BaseListing
from ftw.contentpage.interfaces import IEventListingView
from Products.ATContentTypes.utils import DT2dt
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


def format_date(start, end, wholeday):
    start = DT2dt(start)
    start_date = start.date().strftime('%d.%m.%Y')
    start_time = start.time().strftime('%H:%M')
    end = DT2dt(end)
    end_date = end.date().strftime('%d.%m.%Y')
    end_time = end.time().strftime('%H:%M')
    if wholeday:
        if start_date == end_date:
            return start_date
        return '%s - %s' % (start_date, end_date)
    if start_date == end_date:
        if start_time == end_time:
            return '%s %s' % (start_date, start_time)
        return '%s %s - %s' % (start_date, start_time, end_time)
    return '%s %s - %s %s' % (
          start_date, start_time, end_date, end_time)


class EventListing(BaseListing):
    implements(IEventListingView)

    template = ViewPageTemplateFile("eventlisting.pt")

    def get_items(self):
        # When this import is moved to the top the tests will fail
        # because of a "now()" patching problem in the test..
        from DateTime import DateTime
        query = {'path': '/'.join(self.context.getPhysicalPath()),
                 'portal_type': 'EventPage',
                 'sort_on': 'start',
                 }

        if not self.request.get('archive'):
            query['end'] = {'query': DateTime(), 'range': 'min'}
        return self.search_results(query, 'start')

    def get_date(self, brain):
        obj = brain.getObject()
        return format_date(obj.start(), obj.end(), obj.getWholeDay())
