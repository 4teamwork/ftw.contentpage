from ftw.contentpage.browser.textblock_view import TextBlockView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FAQBlockView(TextBlockView):

    template = ViewPageTemplateFile('faq.pt')
