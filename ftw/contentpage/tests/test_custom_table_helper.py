from ftw.contentpage.browser.listingblock_view import download_link
from ftw.contentpage.testing import ZCML_LAYER
from ftw.testing import MockTestCase


class TestCustomTableHelper(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestCustomTableHelper, self).setUp()

        self.brain = self.stub()
        self.expect(self.brain.getURL()).result('/brain/url')
        self.expect(self.brain.Description).result('Description')

    def test_download_link(self):
        self.replay()
        # Only test if download is appended to the url
        self.assertIn(
            '<a href="%s/download" title="Description">'
            'Title</a>' % self.brain.getURL(),
                download_link(icon=False)(self.brain, 'Title'))
