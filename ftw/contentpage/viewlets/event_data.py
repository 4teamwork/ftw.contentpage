from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EventDataViewlet(ViewletBase):

    index = ViewPageTemplateFile("event_data.pt")

    def has_img(self):
        return bool(self.context.getImage())

    def get_img(self):
        scale = self.context.restrictedTraverse('@@images')
        return scale.scale(
            'image',
            width=100,
            height=100).tag(**{'class': 'tileImage'})
