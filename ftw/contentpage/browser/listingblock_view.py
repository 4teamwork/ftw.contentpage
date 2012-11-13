from Products.Five.browser import BrowserView
from zope.component import queryUtility
from zope.component import getMultiAdapter
from ftw.table.interfaces import ITableGenerator
from ftw.table.interfaces import ITableSource
from ftw.table.catalog_source import DefaultCatalogTableSourceConfig
from ftw.contentpage import _
from ftw.table import helper


class ListingBlockView(BrowserView):
    """Block representation of ListingBlock"""

    def __init__(self, context, request):
        super(ListingBlockView, self).__init__(context, request)
        self.depth = 1
        self.types = ['File', 'Image']
        self.sort_order = 'asc'
        self.sort_on = 'sortable_title'

    @property
    def columns(self):
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
    def table_source(self):
        try:
            return self._table_source
        except AttributeError:
            self._table_source = getMultiAdapter((self, self.request),
                                                 ITableSource)
            return self._table_source

    def update(self):
        # build the query
        query = self.table_source.build_query()

        # search
        results = self.table_source.search_results(query)
        results = self.custom_sort(results, self.sort_on, self.sort_reverse)

        self.contents = results

    def custom_sort(self, results, sort_on, sort_reverse):
        """Custom sort method.
        """

        if getattr(self, '_custom_sort_method', None) is not None:
            results = self._custom_sort_method(results, sort_on, sort_reverse)

        return results

    def render_table(self):
        self.update()

        generator = queryUtility(ITableGenerator, 'ftw.tablegenerator')

        return generator.generate(self.contents,
                                  self.columns,
                                  sortable=True,
                                  selected=(self.sort_on, self.sort_order))

    def update_config(self):
        DefaultCatalogTableSourceConfig.update_config(self)
        self.filter_path = '/'.join(self.context.getPhysicalPath())
