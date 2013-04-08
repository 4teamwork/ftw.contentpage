from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from DateTime.interfaces import SyntaxError as dtSytaxError


class EventListing(BrowserView):
    template = ViewPageTemplateFile("eventlisting.pt")

    def __call__(self):
        return self.template()

    def getEvents(self):
        if not self.request.get('archiv'):
            cat = getToolByName(self.context, 'portal_catalog')
            query = {'path':'/'.join(self.context.getPhysicalPath()), 'portal_type':'EventPage', 'sort_on':'start', 'sort_limit':5}
            events = cat.searchResults(query)
            return events[0:5]
        else:
            cat = getToolByName(self.context, 'portal_catalog')
            query = {'path':'/'.join(self.context.getPhysicalPath()), 'portal_type':'EventPage', 'sort_on':'start'}
            extend_query_by_date(query, self.request.get('archiv'))
            events = cat.searchResults(query)
            return events

    def getDate(self, brain):
        obj = brain.getObject()
        return obj.getDate()

    def has_img(self, brain):
        obj = brain.getObject()
        return obj.getImage()

    def get_img(self, brain):
        obj = brain.getObject()
        scale = obj.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=100,
            height=100).tag(**{'class': 'tileImage'})

def extend_query_by_date(query, datestring):
    try:
        start = DateTime(datestring)
    except dtSytaxError:
        return
    end = DateTime('%s/%s/%s' % (start.year() + start.month() / 12,
                                 start.month() % 12 + 1, 1))
    end = end - 1
    query['start'] = {'query': (start.earliestTime(),
                                    end.latestTime()),
                          'range': 'minmax'}
