from simplelayout.base.viewlets import SimpleLayoutListingViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SimpleLayoutNewsListingViewlet(SimpleLayoutListingViewlet):

    render = ViewPageTemplateFile('teaser_listing_viewlet.pt')

    def getSimpleLayoutContents(self,):
        # Return just himself if there is a descritpion or an image
        if self.context.Description() or self.context.getImage():
            return [self.context, ]
        return []
