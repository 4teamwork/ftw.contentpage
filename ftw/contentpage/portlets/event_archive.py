from ftw.contentpage.interfaces import IEventListingView
from ftw.contentpage.portlets.base_archive_portlet import ArchiveSummary
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class IEventArchive(IPortletDataProvider):
    """Archive portlet interface.
"""


class Assignment(base.Assignment):
    implements(IEventArchive)

    @property
    def title(self):
        return "Event Archive Portlet"


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data
        self.request = request
        self.view = view

    @property
    def available(self):
        """Only show the portlet:
        - If there are Events
        - If view is EventListing
        """
        has_events = bool(self.archive_summary())

        if IEventListingView.providedBy(self.view):
            return has_events
        else:
            return False

    @memoize
    def archive_summary(self):
        return ArchiveSummary(self.context,
                               self.request,
                               ['ftw.contentpage.interfaces.IEventPage'],
                               'start',
                               'event_listing'
                               )()

    render = ViewPageTemplateFile('event_archive.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
