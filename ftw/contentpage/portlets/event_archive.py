from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from ftw.contentpage.portlets.base_archive_portlet import archive_summary


class IEventArchive(IPortletDataProvider):
    """Archive portlet interface.
"""


class Assignment(base.Assignment):
    implements(IEventArchive)

    @property
    def title(self):
        return "Event Archive Portlet"


class Renderer(base.Renderer):

    @property
    def available(self):
        """Only show the portlet, if there are News
        """
        return bool(self.archive_summary())

    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data
        self.request = request


    @memoize
    def archive_summary(self):
        return archive_summary(self.context, self.request, 'EventPage', 'start')

    render = ViewPageTemplateFile('event_archive.pt')

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
