from Products.TinyMCE.browser.atanchors import ATAnchorView


class ContentPageAnchorView(ATAnchorView):

    def listAnchorNames(self, *args, **kwargs):
        query = {'object_provides': 'simplelayout.base.interfaces.'
                                    'ISimpleLayoutBlock'}

        anchors = []
        for block in self.context.listFolderContents(contentFilter=query):
            view = block.restrictedTraverse('content_anchors')
            anchors.extend(view.listAnchorNames(*args, **kwargs))

        return anchors
