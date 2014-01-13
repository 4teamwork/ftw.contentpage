from ftw.contentpage.interfaces import IAuthority
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


def get_brain_data(brain):
    return {'title': brain.Title,
            'path': brain.getPath(),
            'url': brain.getURL(),
            'children': []}


def get_parent_path(path):
    return '/'.join(path.rstrip('/').split('/')[:-1])


def make_treeish(data):
    path2node = dict(map(lambda item: (item['path'], item), data))

    tree = []
    for node in data:
        parent_path = get_parent_path(node['path'])
        if parent_path in path2node:
            path2node[parent_path]['children'].append(node)
        else:
            tree.append(node)

    return tree


class AuthoritiesView(BrowserView):

    sort_on = 'getObjPositionInParent'

    def columns(self):
        contents = self.contents()
        half = len(contents) / 2
        num_leftcolumn = getattr(self.context, 'leftcolumn_num_elements', half)

        columns = [{'classes': 'listing-column listing-column-left',
                    'nodes': contents[:num_leftcolumn]},
                   {'classes': 'listing-column listing-column-right',
                    'nodes': contents[num_leftcolumn:]}]
        return columns

    def contents(self):
        brains = self._get_brains()
        brains = filter(lambda brain: not brain.exclude_from_nav, brains)
        data = map(get_brain_data, brains)
        data = make_treeish(data)
        return data

    def get_query(self):
        path = '/'.join(self.context.getPhysicalPath())
        return {'object_provides': IAuthority.__identifier__,
                'sort_on': self.sort_on,
                'path': {'query': path, 'depth': 2}}

    def _get_brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(self.get_query())
