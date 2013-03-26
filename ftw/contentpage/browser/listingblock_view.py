from ftw.contentpage import _
from ftw.table import helper
from ftw.table.interfaces import ITableGenerator
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility


def download_link(icon=True, classes=None, attrs=None, icon_only=False):

    def _helper(item, value):
        url = '%s/download' % item.getURL()
        attrs = {}
        attrs['href'] = url
        attrs['title'] = item.Description
        return helper.linked(item, value, show_icon=icon,
                           attrs=attrs, icon_only=icon_only)
    return _helper


class ListingBlockView(BrowserView):
    """Block representation of ListingBlock"""

    def __init__(self, context, request):
        super(ListingBlockView, self).__init__(context, request)
        self.sort_on = 'sortable_title'
        self.sort_order = 'asc'

    def columns(self):
        columns = (
            {'column': 'getContentType',
             'column_title': _(u'column_type', default=u'Type'),
             'sort_index': 'getContentType',
             'transform': download_link(icon=True, icon_only=True)},

            {'column': 'Title',
             'column_title': _(u'column_title', default=u'Title'),
             'sort_index': 'sortable_title',
             'transform': download_link(icon=False)},

            {'column': 'modified',
             'column_title': _(u'column_modified', default=u'modified'),
             'sort_index': 'modified',
             'transform': helper.readable_date,
             },

            {'column': 'Creator',
             'column_title': _(u'column_creater', default=u'creater'),
             'transform': helper.readable_author,
             },

            {'column': 'getObjSize',
             'column_title': _(u'column_size', default=u'size'),
             })
        return columns

    @property
    def _build_query(self):
        query = {}
        path = '/'.join(self.context.getPhysicalPath())
        query['path'] = {'query': path, 'depth': 1}
        query['sort_on'] = self.context.getSortOn()
        query['sort_order'] = self.context.getSortOrder()
        return query

    def _get_addable_types(self):
        return [fti.id for fti in self.context.allowedContentTypes()]

    def _get_column(self, column):
        for col in self.columns():
            if column == col['column']:
                return col
        return None

    def _filtered_columns(self):
        filtered = []

        for col in self.context.getTableColumns():
            column = self._get_column(col)
            if column:
                filtered.append(column)

        return filtered

    def render_table(self):
        # Use a custom table template, because we don't want a table header id.
        # The id value is moved to a css klass.
        # Reason: It's no allowed to have an id more than once (In case we
        # have more than one Listingblock on one contentpage)
        template = ViewPageTemplateFile('table-custom-template.pt')

        catalog = getToolByName(self.context, 'portal_catalog')
        generator = queryUtility(ITableGenerator, 'ftw.tablegenerator')
        result = catalog(self._build_query)
        return generator.generate(result,
                                  self._filtered_columns(),
                                  sortable=True,
                                  template=template,
                                  options={'table_title': self.context.title},
                                  selected=(self._build_query['sort_on'],
                                            self._build_query['sort_order']))
