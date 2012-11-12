from Products.Five.browser import BrowserView


class ListingBlockView(BrowserView):
    """Block representation of ListingBlock"""

    def render_table(self):
        return ""
