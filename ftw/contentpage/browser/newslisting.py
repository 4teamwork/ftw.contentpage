from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsListing(BrowserView):

    template = ViewPageTemplateFile('newslisting.pt')
    template_rss = ViewPageTemplateFile('newslisting_rss.pt')

    def __call__(self):
        if self.__name__ == 'news_rss_listing':
            return self.template_rss()
        return self.template()

    def get_creator(self, item):
        memberid = item.Creator
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getMemberById(memberid)
        if member:
            return member
        return None

    def get_news(self):
        """Get all news items"""
        context = self.context
        ct = context.portal_type
        query = {}
        query['portal_type'] = 'News'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'

        if ct == 'Topic':
            return context.queryCatalog()
        else:
            return context.getFolderContents(query)

    def has_img(self, news):
        """ Checks if the news have an image. If view is news_archive_listing
        return False, there we dont want to display images.
        """
        if self.__name__ == 'news_archive_listing':
            return False
        return bool(news.getObject().getImage())

    def get_img(self, news):
        obj = news.getObject()
        scale = obj.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=200,
            height=200).tag(**{'class': 'tileImage'})


class NewsArchiveListing(NewsListing):

    def get_news(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        if self.context.portal_type == 'Topic':
            return self.context.queryCatalog()
        return catalog(
            portal_type='News',
            path='/'.join(self.context.getPhysicalPath()),
            sort_on='effective',
            sort_order='reverse')
