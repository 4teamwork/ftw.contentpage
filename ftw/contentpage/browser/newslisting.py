from DateTime import DateTime
from DateTime.interfaces import SyntaxError as dtSytaxError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from ftw.contentpage.browser.baselisting import BaseListing


class NewsListing(BaseListing):

    template = ViewPageTemplateFile('newslisting.pt')

    def __call__(self):
        if self.__name__ == 'news_rss_listing':
            self.template = ViewPageTemplateFile('newslisting_rss.pt')
        return super(NewsListing, self).__call__()

    def get_items(self):
        """Get all news items"""
        query = {}
        query['portal_type'] = 'News'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'

        # Implement archive functionality - used by the archive portlet
        return self.search_results(query, 'effective')
