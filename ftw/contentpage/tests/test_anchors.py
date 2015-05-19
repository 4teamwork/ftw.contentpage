from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from unittest2 import TestCase


class TestAnchors(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    @browsing
    def test_anchors(self, browser):
        """
        This test makes sure that `ContentPageAnchorView` is able
        to extract the anchors form the text blocks of a content page.
        """
        contentpage = create(Builder('content page').titled('The Page'))
        create(Builder('text block')
               .within(contentpage)
               .having(text="<p>Lorem <a name='anchor-textblock1'></a> "
                            "ipsum dolor sit amet.</p>"))
        create(Builder('text block')
               .within(contentpage)
               .having(text="<p>Lorem <a name='anchor-textblock2'></a> "
                            "ipsum dolor sit amet.</p>"))

        view = contentpage.restrictedTraverse('content_anchors')
        anchor_names = view.listAnchorNames()
        self.assertEqual(['anchor-textblock1', 'anchor-textblock2'],
                         anchor_names)
