from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EventDataViewlet(ViewletBase):

    index = ViewPageTemplateFile("event_data.pt")

    def has_img(self):
        return False
