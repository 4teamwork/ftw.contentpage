from simplelayout.base.viewlets import SimpleLayoutListingViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from simplelayout.base.interfaces import ISimpleLayoutCapable


class SimpleLayoutNewsListingViewlet(SimpleLayoutListingViewlet):

    render = ViewPageTemplateFile('teaser_listing_viewlet.pt')

    def getSimpleLayoutContents(self,):
        # Return just himself
        parent = self.context.aq_parent
        # XXX: Is this still necessary
        if not ISimpleLayoutCapable.providedBy(parent):
            return []

        return [self.context, ]
