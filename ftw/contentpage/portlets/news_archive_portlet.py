from ftw.contentpage.interfaces import INewsListingView
from ftw.contentpage.portlets.base_archive_portlet import ArchiveSummary
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class INewsArchivePortlet(IPortletDataProvider):
    """Archive portlet interface.
"""


class Assignment(base.Assignment):
    implements(INewsArchivePortlet)

    @property
    def title(self):
        return "News Archive Portlet"


class Renderer(base.Renderer):
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data
        self.request = request
        self.view = view

    @property
    def available(self):
        """Only show the portlet:
        - If there are News
        - If view is NewsListing
        """
        has_news = bool(self.archive_summary())

        if INewsListingView.providedBy(self.view):
            return has_news
        else:
            return False

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
        return ArchiveSummary(
            self.context,
            self.request,
            ['ftw.contentpage.interfaces.INews'],
            'effective',
            'newslisting')()

    render = ViewPageTemplateFile('news_archive_portlet.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
