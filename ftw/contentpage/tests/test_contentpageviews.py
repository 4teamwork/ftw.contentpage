from ftw.testing import MockTestCase
from ftw.contentpage.testing import ZCML_LAYER
from ftw.contentpage.interfaces import IContentPage
from zope.component import getMultiAdapter
from mocker import ANY
from mocker import KWARGS


class TestContentPageListingViews(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestContentPageListingViews, self).setUp()

        self.context = self.providing_stub(IContentPage)
        self.request = self.stub_request()

        # Mock getFolderContents
        self.brain1 = self.stub()
        self.expect(self.brain1.exclude_from_nav).result(False)
        self.brain2 = self.stub()
        self.expect(self.brain2.exclude_from_nav).result(False)
        self.brain3 = self.stub()
        self.expect(self.brain3.exclude_from_nav).result(False)
        self.brain4 = self.stub()
        self.expect(self.brain4.exclude_from_nav).result(False)
        self.expect(self.context.getFolderContents(ANY)).result(
            [self.brain1, self.brain2])

    def test_authorities_view(self):
        catalog = self.stub()
        self.mock_tool(catalog, 'portal_catalog')
        self.expect(
            catalog(KWARGS, path={'query': '/path1', 'depth': 1})).result(
                [self.brain3, ])
        self.expect(
            catalog(KWARGS, path={'query': '/path2', 'depth': 1})).result(
                [self.brain4, ])

        self.replay()

        view = getMultiAdapter((self.context, self.request),
                               name='authorities_view')

        self.assertEquals(view.contents(), {'leftcolumn': [self.brain1, ],
                                            'rightcolumn': [self.brain2]})

        self.assertEquals(view.subcontents('/path1'), [self.brain3, ])
        self.assertEquals(view.subcontents('/path2'), [self.brain4, ])

    def test_authorities_view_leftcolumn_num_elements(self):
        self.replay()

        setattr(self.context, 'leftcolumn_num_elements', 2)

        view = getMultiAdapter((self.context, self.request),
                               name='authorities_view')
        self.assertEquals(view.contents(), {'leftcolumn':
                                                [self.brain1, self.brain2],
                                            'rightcolumn': []})
