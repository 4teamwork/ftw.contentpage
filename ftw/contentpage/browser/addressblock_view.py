from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.geo.geographer.interfaces import IGeoreferenced
from collective.geo.mapwidget.browser.widget import MapWidget
from ftw.contentpage.interfaces import IAddressBlockView
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements


class AddressBlockView(BrowserView):
    """Block representation of AddressBlock"""
    implements(IAddressBlockView)

    address_ptl = ViewPageTemplateFile('address.pt')

    def get_address_as_html(self):
        html = [self.context.getAddress()]
        if self.context.getExtraAddressLine():
            html.append(self.context.getExtraAddressLine())
        return '<br />'.join(html)

    def address(self):
        return self.address_ptl()

    def get_address_map(self):
        address_map = MapWidget(self, self.request, self.context)
        address_map.mapid = "geo-%s" % self.context.getId()
        address_map.addClass('addressblock-map')

        return address_map

    def show_map(self):
        return IGeoreferenced(self.context).hasCoordinates()


class AddressBlockPortletView(AddressBlockView):
    """Block representation of AddressBlock"""

    def has_team(self):
        result = aq_parent(aq_inner(self.context)).getFolderContents(
            contentFilter={'portal_type': 'ContentPage',
                           'id': 'team'})
        return bool(result)


class AddressBlockDetailView(AddressBlockView):
    """AddressBlock detail View"""
