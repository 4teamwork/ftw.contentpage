from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from plone.indexer.wrapper import IndexableObjectWrapper


class TestSnippetText(TestCase):
    
    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        self.page = portal[portal.invokeFactory('ContentPage', 'page',
            title=u"The ContentPage Title",
            description=u"The ContentPage Description")]
        self.wrapped = IndexableObjectWrapper(self.page, portal.portal_catalog)

    def test_contentpage_id_not_in_snippettext(self):
        self.assertNotIn('page', self.wrapped.snippetText)

    def test_contentpage_title_not_in_snippettext(self):
        self.assertNotIn("The ContentPage Title", self.wrapped.snippetText)

    def test_contentpage_description_in_snippetttext(self):
        self.assertIn("The ContentPage Description", self.wrapped.snippetText)

    def test_textblock_title_and_id_not_in_snippettext(self):
        self.page.invokeFactory('TextBlock', 'block',
            title=u'The TextBlock Title')
        self.assertNotIn('block', self.wrapped.snippetText)
        self.assertNotIn('The TextBlock Title', self.wrapped.snippetText)

    def test_textblock_title_in_snippettext_if_visible(self):
        self.page.invokeFactory('TextBlock', 'block',
            title=u'The TextBlock Title', showTitle=True)
        self.assertIn('The TextBlock Title', self.wrapped.snippetText)

    def test_textblock_text_in_snippettext(self):
        self.page.invokeFactory('TextBlock', 'block',
            text=u'The TextBlock Text')
        self.assertIn('The TextBlock Text', self.wrapped.snippetText)

    def test_addressblock_fields_in_snippettext(self):
        self.page.invokeFactory('AddressBlock', 'block',
            address=u'1st Avenue', city='Gotham City')
        self.assertIn('1st Avenue', self.wrapped.snippetText)
        self.assertIn('Gotham City', self.wrapped.snippetText)

    def test_contentpage_in_contentpage_is_ignored_in_snippettext(self):
        self.page.invokeFactory('ContentPage', 'subpage',
            description="A ContentPage in a ContentPage")
        self.assertNotIn("A Contentpage in a ContentPage",
                         self.wrapped.snippetText)
