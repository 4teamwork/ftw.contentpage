from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from ftw.contentpage.interfaces import IOrgUnitMarker


class AuthoritiesView(BrowserView):

    sort_on = 'getObjPositionInParent'

    def contents(self):
        context = self.context
        results = context.getFolderContents(
            {'object_provides': IOrgUnitMarker.__identifier__,
             'sort_on': self.sort_on})
        results = [res for res in results if not res.exclude_from_nav]
        contents = {}
        half = len(results) / 2
        half = getattr(self.context, 'leftcolumn_num_elements', half)
        contents['leftcolumn'] = results[:half]
        contents['rightcolumn'] = results[half:]
        return contents

    def subcontents(self, path):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        query = {}
        query['sort_on'] = self.sort_on
        query['path'] = {'query': path, 'depth': 1}
        query['object_provides'] = IOrgUnitMarker.__identifier__
        results = catalog(**query)
        return [res for res in results if not res.exclude_from_nav]
