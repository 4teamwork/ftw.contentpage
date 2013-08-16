from ftw.contentpage.browser.textblock_view import TextBlockView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class FAQBlockView(TextBlockView):

    template = ViewPageTemplateFile('faq.pt')

    def __call__(self):
        self.request['viewname'] = 'faq'
        self.portal_url = getToolByName(self.context, "portal_url")()
        return self.template()
