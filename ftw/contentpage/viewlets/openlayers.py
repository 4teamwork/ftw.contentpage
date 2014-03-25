from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OpenlayersViewlet(ViewletBase):
    index = ViewPageTemplateFile('openlayers.pt')

    def available(self):
        return bool(self.context.getFolderContents({
            'portal_type': 'AddressBlock'}))
