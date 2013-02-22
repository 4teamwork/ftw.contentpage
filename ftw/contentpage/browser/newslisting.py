from Products.CMFPlone.PloneBatch import Batch
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsListing(BrowserView):

    template = ViewPageTemplateFile('newslisting.pt')
    template_rss = ViewPageTemplateFile('newslisting_rss.pt')

    def __call__(self):
        b_start = self.request.form.get('b_start',0)
        self.batch = Batch(self.get_news(), 10,
                           b_start)
        if self.__name__ == 'news_rss_listing':
            return self.template_rss()
        return self.template()

    def get_creator(self, item):
        memberid = item.Creator
        mt = getToolByName(self.context, 'portal_membership')
        member_info = mt.getMemberInfo(memberid)
        if member_info:
            fullname = member_info.get('fullname', '')
        else:
            fullname = None
        if fullname:
            return fullname
        else:
            return memberid

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
        """ Checks if the news have an image.
        """
        return bool(news.getObject().getImage())

    def get_img(self, news):
        obj = news.getObject()
        scale = obj.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=100,
            height=100).tag(**{'class': 'tileImage'})
