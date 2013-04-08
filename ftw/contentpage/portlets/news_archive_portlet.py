from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from ftw.contentpage.portlets.base_archive_portlet import archive_summary

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

    @property
    def available(self):
        """Only show the portlet, if there are News
        """
        return bool(self.archive_summary())

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
        return archive_summary(self.context, self.request, 'News', 'effective')

    render = ViewPageTemplateFile('news_archive_portlet.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
