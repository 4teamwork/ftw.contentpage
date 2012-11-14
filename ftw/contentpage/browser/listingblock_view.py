from ftw.contentpage import _
from ftw.table import helper
from ftw.table.interfaces import ITableGenerator
from Products.Five.browser import BrowserView
from zope.component import queryUtility
from Products.CMFPlone.utils import getToolByName


class ListingBlockView(BrowserView):
    """Block representation of ListingBlock"""

    def __init__(self, context, request):
        super(ListingBlockView, self).__init__(context, request)
        self.sort_on = 'sortable_title'
        self.sort_order = 'asc'

    def _columns(self):
        columns = (
            {'column': 'Title',
             'column_title': _(u'column_title', default=u'Title'),
             'sort_index': 'sortable_title',
             'transform': helper.link(icon=True, tooltip=True)},

            {'column': 'modified',
             'column_title': _(u'column_modified', default=u'modified'),
             'transform': helper.readable_date,
             'width': 80})
        return columns

    @property
    def _build_query(self):
        query = {}
        path = '/'.join(self.context.getPhysicalPath())
        query['path'] = {'query': path, 'depth': 1}
        query['portal_type'] = self._get_addable_types()
        query['sort_on'] = 'sortable_title'
        query['sort_order'] = 'asc'
        return query

    def _get_addable_types(self):
        return [fti.id for fti in self.context.allowedContentTypes()]

    def render_table(self):

        catalog = getToolByName(self.context, 'portal_catalog')
        generator = queryUtility(ITableGenerator, 'ftw.tablegenerator')
        result = catalog(self._build_query)
        return generator.generate(result,
                                  self._columns(),
                                  sortable=True,
                                  selected=(self._build_query['sort_on'],
                                            self._build_query['sort_order']))
