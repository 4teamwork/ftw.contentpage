from simplelayout.base.viewlets import SimpleLayoutListingViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SimpleLayoutNewsListingViewlet(SimpleLayoutListingViewlet):

    render = ViewPageTemplateFile('simplelayout_news_listing_viewlet.pt')

    def getSimpleLayoutContents(self,):
        # Return just himself
        return [self.context, ]

