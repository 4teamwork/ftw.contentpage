from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class EventListing(BrowserView):
    template = ViewPageTemplateFile("eventlisting.pt")

    def __call__(self):
        return self.template()

    def getEvents(self):
        cat = getToolByName(self.context, 'portal_catalog')
        query = {'path':'/'.join(self.context.getPhysicalPath()), 'portal_type':'Event'}
        events = cat.search(query)
        return events

    def getDate(self):
        import pdb; pdb.set_trace()

    def has_img(self):
        return False
