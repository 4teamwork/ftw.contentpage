from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from simplelayout.base.interfaces import ISimplelayoutView
from simplelayout.base.viewlets import SimpleLayoutListingViewlet


class SimpleLayoutNewsListingViewlet(SimpleLayoutListingViewlet):

    render = ViewPageTemplateFile('teaser_listing_viewlet.pt')

    def available(self):
        if not ISimplelayoutView.providedBy(self.view):
            return False

        if self.context.Description() or self.context.getImage():
            return True

        return False
