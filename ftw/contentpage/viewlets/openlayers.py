from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class OpenlayersViewlet(ViewletBase):
    index = ViewPageTemplateFile('openlayers.pt')
