from ftw.contentpage.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from zope.component import getMultiAdapter
from ftw.contentpage.interfaces import IAddressBlock
from simplelayout.base.interfaces import ISimpleLayoutCapable
from ftw.contentpage.interfaces import IFtwContentPageLayer
from mocker import ANY


class TestAddressBlockView(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestAddressBlockView, self).setUp()

        self.request = self.stub_request(IFtwContentPageLayer)
        self.context = self.providing_stub(IAddressBlock)
        self.expect(self.context.getAddress()).result("Address line")
        self.expect(self.context.getExtraAddressLine()).result(
            "Additional line")

    def test_component_registered_block_view(self):
        self.replay()
        self.assertNotEquals(getMultiAdapter(
            (self.context, self.request), name="block_view"),
            None)

    def test_component_registered_portlet_view(self):
        self.replay()
        self.assertNotEquals(getMultiAdapter(
            (self.context, self.request), name="block_view-portlet"),
            None)

    def test_component_registered_detail_view(self):
        self.replay()
        self.assertNotEquals(getMultiAdapter(
            (self.context, self.request), name="addressblock_detail_view"),
            None)

    def test_get_address_as_html(self):
        self.replay()
        view = getMultiAdapter((self.context, self.request),
                               name="block_view")
        self.assertEquals(view.get_address_as_html(),
                          "Address line<br />Additional line")

    def test_has_team(self):
        parent = self.providing_stub(ISimpleLayoutCapable)
        self.set_parent(self.context, parent)
        self.expect(parent.getFolderContents(contentFilter=ANY)).result(True)
        self.replay()
        view = getMultiAdapter(
            (self.context, self.request), name="block_view-portlet")
        self.assertTrue(view.has_team())

    def test_has_no_team(self):
        parent = self.providing_stub(ISimpleLayoutCapable)
        self.set_parent(self.context, parent)
        self.expect(parent.getFolderContents(contentFilter=ANY)).result(
            False)
        self.replay()
        view = getMultiAdapter(
            (self.context, self.request), name="block_view-portlet")
        self.assertFalse(view.has_team())
