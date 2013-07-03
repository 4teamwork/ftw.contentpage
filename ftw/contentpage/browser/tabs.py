from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TabbedBlockView(BrowserView):
    template = ViewPageTemplateFile('tabs.pt')

    def __call__(self):
        return self.template()

    def children(self):
        return self.context.getFolderContents(
            contentFilter={'object_provides': 'simplelayout.base.interfaces.IOneColumn'},
            full_objects=True)
