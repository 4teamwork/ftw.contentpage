from ftw.contentpage.content.schema import DEFAULT_TO_HIDE
from ftw.contentpage.content.schema import finalize
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.CMFCore.permissions import ManagePortal
from unittest2 import TestCase


class TestAddressBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestAddressBlockCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

    def test_finalize_schema(self):
        schema = ATContentTypeSchema.copy()
        finalize(schema)

        for name in DEFAULT_TO_HIDE:
            if name in schema:
                self.assertEquals(ManagePortal, schema[name].write_permission)
                self.assertEquals({'view': 'invisible', 'edit': 'invisible'},
                                  schema[name].widget.visible)

        self.assertTrue(schema['excludeFromNav'].default)

    def test_finalize_schema_additional_hide(self):
        schema = ATContentTypeSchema.copy()
        finalize(schema, hide=['title'])

        self.assertEquals(ManagePortal, schema['title'].write_permission)
        self.assertEquals({'view': 'invisible', 'edit': 'invisible'},
                          schema['title'].widget.visible)

    def test_finalize_schema_do_not_hide(self):
        schema = ATContentTypeSchema.copy()
        finalize(schema, show=['subject'])

        self.assertNotEqual(ManagePortal, schema['subject'].write_permission)
        self.assertNotEquals({'view': 'invisible', 'edit': 'invisible'},
                             schema['subject'].widget.visible)

    def test_finalize_schema_show_inextisting_field(self):
        schema = ATContentTypeSchema.copy()
        # I'm not realy sure what to test
        self.assertNotIn('dummy', schema)
        finalize(schema, show=['dummy'])
        self.assertNotIn('dummy', schema)
