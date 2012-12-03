from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from simplelayout.base.interfaces import ISimpleLayoutBlock
from unittest2 import TestCase


class TestTextBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestTextBlockCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()

    def _create_textblock(self):
        textblock = self.contentpage.get(
            self.contentpage.invokeFactory('TextBlock', 'textblock'))
        # Fire all necessary events
        textblock.processForm()
        return textblock

    def test_fti(self):
        self.assertIn('TextBlock', self.portal.portal_types.objectIds())

    def test_creation(self):
        _id = self.contentpage.invokeFactory('TextBlock', 'textblock')
        self.assertIn(_id, self.contentpage.objectIds())

    def test_simplelayout_integration(self):
        textblock = self._create_textblock()
        ISimpleLayoutBlock.providedBy(textblock)

    def test_set_title(self):
        textblock = self._create_textblock()
        textblock.REQUEST.set('text', '<p>text</p>')
        textblock.setTitle(None)
        self.assertEquals(textblock.Title(), 'text')

        textblock.setTitle('title')
        self.assertEquals(textblock.Title(), 'title')

        # Crop after 30 chars
        text = "*" * 35
        textblock.REQUEST.set('text', text)
        textblock.setTitle(None)
        self.assertEquals(textblock.Title(), "*" * 30)

    def tearDown(self):
        super(TestTextBlockCreation, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
