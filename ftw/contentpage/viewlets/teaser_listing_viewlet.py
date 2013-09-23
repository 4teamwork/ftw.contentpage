from simplelayout.base.viewlets import SimpleLayoutListingViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SimpleLayoutNewsListingViewlet(SimpleLayoutListingViewlet):

    render = ViewPageTemplateFile('teaser_listing_viewlet.pt')

    def available(self):
        if self.context.Description() or self.context.getImage():
            return True

        return False
