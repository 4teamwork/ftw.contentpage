from ftw.contentpage.browser.baselisting import BaseListing
from ftw.contentpage.interfaces import INewsListingView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class NewsListing(BaseListing):
    implements(INewsListingView)

    default_template = ViewPageTemplateFile('newslisting.pt')
    rss_template = ViewPageTemplateFile('newslisting_rss.pt')

    @property
    def template(self):
        if self.__name__ == 'news_rss_listing':
            return self.rss_template
        else:
            return self.default_template

    def show_author(self):
        """Checks if the user is anonymous and is not allowAnonymousViewAbout.
        """
        site_props = getToolByName(self.context, 'portal_properties').site_properties
        mt = getToolByName(self.context, 'portal_membership')

        if not site_props.getProperty('allowAnonymousViewAbout', False) \
                and mt.isAnonymousUser():
            return False
        return True

    def get_items(self):
        """Get all news items"""
        query = {}
        query['object_provides'] = 'ftw.contentpage.interfaces.INews'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'

        # Implement archive functionality - used by the archive portlet
        return self.search_results(query, 'effective')
