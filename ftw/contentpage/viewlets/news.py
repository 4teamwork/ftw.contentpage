from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsDate(ViewletBase):

    index = ViewPageTemplateFile("news_date.pt")
