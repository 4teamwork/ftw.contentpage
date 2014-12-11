import transaction
from ftw.builder import Builder, create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.registry.interfaces import IRegistry
from unittest2 import TestCase
from zope.component import getUtility


class TestListingBlockTableHelper(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        content_page = create(Builder('content page'))
        self.listing_block = create(Builder('listing block').within(content_page))
        self.file_ = create(Builder('file')
                            .with_dummy_content()
                            .having(description='S\xc3\xb6me description')
                            .within(self.listing_block))

    @browsing
    def test_file_link_default_value(self, browser):
        browser.login().visit(self.listing_block, view='block_view')
        self.assertEquals(
            self.file_.absolute_url() + '/download',
            browser.css('.linkWrapper a').first.attrib['href']
        )

    @browsing
    def test_file_link_empty_registry_value_without_trailing_slash(self, browser):
        registry = getUtility(IRegistry)
        registry['ftw.contentpage.listingblock.defaultfileviewname'] = u''
        transaction.commit()

        browser.login().visit(self.listing_block, view='block_view')
        self.assertEquals(
            self.file_.absolute_url(),
            browser.css('.linkWrapper a').first.attrib['href']
        )

    @browsing
    def test_file_link_changed_registry_value(self, browser):
        registry = getUtility(IRegistry)
        registry['ftw.contentpage.listingblock.defaultfileviewname'] = u'some-viewname'
        transaction.commit()

        browser.login().visit(self.listing_block, view='block_view')
        self.assertEquals(
            self.file_.absolute_url() + '/some-viewname',
            browser.css('.linkWrapper a').first.attrib['href']
        )
