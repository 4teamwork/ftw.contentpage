from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime
from ftw.contentpage.browser.baselisting import BaseListing
from Products.ATContentTypes.utils import DT2dt


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
        return '%s %s - %s' % (start_date, start_time, end_time)
    return '%s %s - %s %s' % (
          start_date, start_time, end_date, end_time)


class EventListing(BaseListing):

    template = ViewPageTemplateFile("eventlisting.pt")

    def get_items(self):
        query = {'path': '/'.join(self.context.getPhysicalPath()),
                 'portal_type': 'EventPage',
                 'sort_on': 'start',
                 'start': {'query': DateTime(), 'range': 'min'}
                 }
        return self.search_results(query, 'start')

    def get_date(self, brain):
        obj = brain.getObject()
        return format_date(obj.start(), obj.end(), obj.getWholeDay())
