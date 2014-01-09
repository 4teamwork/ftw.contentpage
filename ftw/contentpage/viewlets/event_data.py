from ftw.contentpage.browser.eventlisting import format_date
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EventDataViewlet(ViewletBase):

    index = ViewPageTemplateFile("event_data.pt")

    def get_date(self):
        return format_date(self.context.start(), self.context.end(),
                           self.context.getWholeDay())
    
    def get_location(self):
        return self.context.getField('location').get(self.context)
        