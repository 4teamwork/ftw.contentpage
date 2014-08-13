from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from simplelayout.base.interfaces import ISimpleLayoutBlock
from unittest2 import TestCase
from zope.component import getUtility
from zope.component import queryMultiAdapter
from plone.registry import Record, field


class TestListingBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestListingBlockCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

    def _create_listingblock(self):
        listingblock = self.contentpage.get(
            self.contentpage.invokeFactory('ListingBlock', 'listingblock'))
        # Fire all necessary events
        listingblock.processForm()

        return listingblock

    def test_fti(self):
        self.assertIn('ListingBlock', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.contentpage.invokeFactory('ListingBlock', 'listingblock')
        self.assertIn(_id, self.contentpage.objectIds())

    def test_simplelayout_integration(self):
        listingblock = self._create_listingblock()
        ISimpleLayoutBlock.providedBy(listingblock)

    def test_exclude_from_nav(self):
        listingblock = self._create_listingblock()
        self.assertTrue(listingblock.getExcludeFromNav())

    def test_get_columns(self):
        listingblock = self._create_listingblock()
        self.assertEquals(
            ['getContentType', 'Title', 'modified', 'Creator',
             'getObjSize', 'review_state', 'id'],
            listingblock.getColumns().keys())
        self.assertEquals(
            ['column_type', 'column_title', 'column_modified',
             'column_creater', 'column_size', 'review_state', 'ID'],
            listingblock.getColumns().values())

    def test_default_title(self):
        listingblock = self._create_listingblock()
        # Default is empty
        self.assertEquals('', listingblock.Title())

    def test_can_set_default_page(self):
        listingblock = self._create_listingblock()
        self.assertFalse(listingblock.canSetDefaultPage())

    def test_change_default_title(self):
        registry = getUtility(IRegistry)
        registry.records['ftw.contentpage.listingblock.defaulttitle'] = \
            Record(field.TextLine(title=u"dummy", default=u"N/A"),
                   value=u'Downloads')

        listingblock = self._create_listingblock()
        self.assertEquals('Downloads', listingblock.Title())

    def test_default_table_columns(self):
        registry = getUtility(IRegistry)

        registry.records[
            'ftw.contentpage.listingblock.defaulttablecolumns'].value = \
            (u'Creator', u'Title', u'BadColumn')

        listingblock = self._create_listingblock()

        view = queryMultiAdapter((listingblock, listingblock.REQUEST),
                                 name='block_view')

        content = view.render_table()

        self.assertIn(u'Creator', content)
        self.assertIn(u'Title', content)
        self.assertNotIn(u'BadColumn', content)

    def test_sort_index_vocabulary(self):
        listingblock = self._create_listingblock()

        self.assertEquals(listingblock.getSortIndexVocabulary().keys(),
            ['getContentType', 'sortable_title', 'modified',
             'id', 'getObjPositionInParent'])

    def tearDown(self):
        super(TestListingBlockCreation, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
