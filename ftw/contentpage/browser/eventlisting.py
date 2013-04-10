from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from DateTime.interfaces import SyntaxError as dtSytaxError
from ftw.contentpage.browser.baselisting import BaseListing


class EventListing(BaseListing):

    template = ViewPageTemplateFile("eventlisting.pt")

    def get_items(self):
            query = {'path': '/'.join(self.context.getPhysicalPath()),
                     'portal_type': 'EventPage',
                     'sort_on': 'start',
                     'start': {'query': DateTime(), 'range': 'min'}
                     }
            return self.search_results(query, 'start')

    def getDate(self, brain):
        obj = brain.getObject()
        return obj.getDate()
