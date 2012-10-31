from Products.Five.browser import BrowserView
from Acquisition import aq_inner, aq_parent


class AddressBlockView(BrowserView):
    """Block representation of AddressBlock"""

    def get_address_as_html(self):
        html = [self.context.getAddress()]
        if self.context.getExtraAddressLine():
            html.append(self.context.getExtraAddressLine())
        return '<br />'.join(html)

    def get_opening_hours_as_html(self):
        """returns the opening hours as html
        """
        return self.context.getOpeningHours().replace('\n', '<br />')


class AddressBlockPortletView(AddressBlockView):
    """Block representation of AddressBlock"""

    def has_team(self):
        result = aq_parent(aq_inner(self.context)).getFolderContents(
            contentFilter={'portal_type': 'ContentPage',
                           'id': 'team'})
        return bool(result)
