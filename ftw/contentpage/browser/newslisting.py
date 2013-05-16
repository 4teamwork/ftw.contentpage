from ftw.contentpage.browser.baselisting import BaseListing
from ftw.contentpage.interfaces import INewsListingView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class NewsListing(BaseListing):
    implements(INewsListingView)

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
