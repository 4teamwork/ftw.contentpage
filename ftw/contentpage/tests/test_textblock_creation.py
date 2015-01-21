from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.testbrowser.pages import statusmessages
from simplelayout.base.interfaces import ISimpleLayoutBlock
from unittest2 import TestCase


class TestTextBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.contentpage = create(Builder('content page').titled('The Page'))

    def test_simplelayout_integration(self):
        textblock = create(Builder('text block').within(self.contentpage))
        ISimpleLayoutBlock.providedBy(textblock)

    @browsing
    def test_text_is_used_as_title(self, browser):
        browser.login().open(self.contentpage)
        factoriesmenu.add('TextBlock')
        browser.fill({'Text': '<p>Hello World</p>'}).save()
        statusmessages.assert_no_error_messages()
        block = self.contentpage.objectValues()[0]
        self.assertEquals('Hello World', block.Title())

    @browsing
    def test_title_is_cropped_chars_when_filled_with_text(self, browser):
        browser.login().open(self.contentpage)
        factoriesmenu.add('TextBlock')
        browser.fill({'Text': '<p>%s</p>' % ('X' * 50)}).save()
        statusmessages.assert_no_error_messages()
        block = self.contentpage.objectValues()[0]
        self.assertEquals(29, len(block.Title()))

    @browsing
    def test_alt_text_is_image_filename_when_empty(self, browser):
        create(Builder('text block')
               .within(self.contentpage)
               .with_dummy_content()
               .having(text='<p>Text</p>'))
        browser.login().open(self.contentpage)
        self.assertEqual(
            'image.gif',
            browser.css('.sl-img-wrapper img').first.attrib['alt'])
