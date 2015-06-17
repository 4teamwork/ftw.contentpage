from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from simplelayout.base.utils import IBlockControl
from unittest2 import TestCase
from zope.component import getUtility
from zope.component import queryMultiAdapter
import os
import transaction


class TestTextBlockView(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestTextBlockView, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()
        self.contentpage.reindexObject()
        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def _create_textblock(self):
        textblock = self.contentpage.get(
            self.contentpage.invokeFactory('TextBlock', 'textblock'))
        # Fire all necessary events
        textblock.processForm()
        transaction.commit()
        return textblock

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_addressblock_view(self):
        textblock = self._create_textblock()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn(textblock.getId(), self.browser.contents)
        self.assertIn('simplelayout-block-wrapper TextBlock',
                      self.browser.contents)

    def test_show_title(self):
        textblock = self._create_textblock()
        test_title = 'This is the title'
        textblock.setTitle(test_title)
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')

        self.assertNotIn(test_title, view.index())

        textblock.setShowTitle(True)
        self.assertIn(test_title, view.index())

    def test_text_not_required(self):
        textblock = self._create_textblock()
        test_text = 'This is the Text'
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')

        self.assertNotIn(test_text, view.index())

        textblock.setText(test_text)
        self.assertIn(test_text, view.index())

    def test_has_image(self):
        textblock = self._create_textblock()
        self._auth()
        self.browser.open(self.contentpage.absolute_url())
        self.assertNotIn('sl-img-wrapper', self.browser.contents)

        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')
        self.assertFalse(view.has_image())

        # Add Image
        dummy = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        dummy.seek(0)
        textblock.setImage(dummy)
        textblock.processForm()
        transaction.commit()

        self.assertTrue(view.has_image())

        self.browser.open(self.contentpage.absolute_url())
        self.assertIn('sl-img-wrapper', self.browser.contents)

    def test_get_image_tag(self):
        textblock = self._create_textblock()
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')
        # No image uploaded
        self.assertEquals(view.get_image_tag(), '')

        # Add Image
        dummy = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        dummy.seek(0)
        textblock.setImage(dummy)
        textblock.setImageAltText('image alt text')
        textblock.processForm()

        self.assertIn('alt="image alt text"', view.get_image_tag())
        textblock.setImageCaption('image caption')
        self.assertIn('title="image caption"', view.get_image_tag())

        # Change view
        converter = getUtility(IBlockControl, name='block-layout')
        converter.update(self.contentpage,
                         textblock,
                         self.contentpage.REQUEST,
                         layout='no-image',
                         viewname='block-view')

        self.assertEquals(view.get_image_tag(), '')

    def test_image_wrapper_style(self):
        textblock = self._create_textblock()
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')

        # Add Image
        dummy = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        dummy.seek(0)
        textblock.setImage(dummy)
        textblock.processForm()
        transaction.commit()

        width = view.image_wrapper_style()[7:-2]
        self.assertIn(width, view.get_image_tag())
        self.browser.open(self.contentpage.absolute_url())
        self.assertIn(view.image_wrapper_style(),
                      self.browser.contents)

    def test_image_with_umlauts_in_filename(self):
        textblock = self._create_textblock()
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                  name='block_view')

        with open("%s/dummy.png" % os.path.split(__file__)[0], 'r') as dummy:
            textblock.setImage(dummy)
        textblock.getImage().filename = 'K\xc3\xbcche.png'
        self.assertIn(u'K\xfcche.png', view.get_image_tag())

    def test_get_css_klass(self):
        textblock = self._create_textblock()
        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')

        # Init
        self.assertEquals(view.get_css_klass(), 'sl-img-small')

        # Change view
        converter = getUtility(IBlockControl, name='block-layout')
        converter.update(self.contentpage,
                         textblock,
                         self.contentpage.REQUEST,
                         layout='no-image',
                         viewname='block-view')

        view = queryMultiAdapter((textblock, textblock.REQUEST),
                                 name='block_view')
        self.assertEquals(view.get_css_klass(), 'sl-img-no-image')

    @browsing
    def test_image_caption_not_linked(self, browser):
        """
        The image caption has accidentally been linked to the image
        overlay. This test makes sure that this is no longer the case.
        """
        textblock = self._create_textblock()

        # Add Image
        dummy = open("%s/dummy.png" % os.path.split(__file__)[0], 'r')
        dummy.seek(0)
        textblock.setImage(dummy)
        textblock.setImageAltText('image alt text')
        # Set the image caption, which our test is based on.
        textblock.setImageCaption('image caption')
        # Enable opening the image in an overlay, this generates the link.
        textblock.setImageClickable(True)
        textblock.processForm()
        transaction.commit()

        browser.login().visit(self.contentpage)

        # The caption must not be inside the link.
        self.assertEqual([], browser.css(".sl-img-wrapper a p"))

        # But instead, the image caption must be outside of the link.
        self.assertEqual(['image caption'],
                         browser.css(".sl-img-wrapper p").text)

    def tearDown(self):
        super(TestTextBlockView, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])

        transaction.commit()
