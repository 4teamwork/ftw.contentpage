from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.interfaces import IAuthority
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class TestMarkerInterfaceForListings(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        super(TestMarkerInterfaceForListings, self).setUp()

        self.portal = self.layer['portal']

    def test_contentpage_is_extended_with_checkbox(self):
        page = create(Builder('content page'))

        fieldname = 'mark_as_authority'
        self.assertIn(fieldname,
                      page.Schema().keys(),
                      '{0} nod found in content page schema'.format(fieldname))

    def test_authority_marker_is_set_if_checkbox_is_true(self):
        page = create(Builder('content page'))
        page.Schema()['mark_as_authority'].set(page, True)

        self.assertTrue(IAuthority.providedBy(page),
                        '{0} is not marked for listings'.format(page))

    def test_authority_marker_is_not_set_if_checkbox_is_false(self):
        page = create(Builder('content page'))
        page.Schema()['mark_as_authority'].set(page, False)

        self.assertFalse(IAuthority.providedBy(page),
                         '{0} is marked for listings'.format(page))

    def test_listing_marker_is_not_set_by_default(self):
        page = create(Builder('content page'))

        self.assertFalse(IAuthority.providedBy(page),
                         '{0} is marked for listings'.format(page))

    def test_catalog_is_always_up_to_date(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        page = create(Builder('content page'))

        result = catalog({'object_provides': IAuthority.__identifier__})
        self.assertFalse(result, 'Nothing should be marked by default.')

        page.Schema()['mark_as_authority'].set(page, True)
        page.processForm()

        result = catalog({'object_provides': IAuthority.__identifier__})
        self.assertTrue(result, 'Content should be marked')

        page.Schema()['mark_as_authority'].set(page, False)
        page.processForm()

        result = catalog({'object_provides': IAuthority.__identifier__})
        self.assertFalse(result, 'Nothing should be marked by default.')

    def test_mark_for_listing_permission_default(self):
        permission = 'ftw.contentpage: Toggle IAuthority marker interface'

        roles = [r['name'] for r in self.portal.rolesOfPermission(permission) if r[
            'selected']]
        self.assertEquals(roles,
                          ['Contributor', 'Manager'],
                          'Manager and Contributor should have the permission:'
                           ' {0}'.format(
                              permission))

    def test_mark_for_listing_permission(self):
        page = create(Builder('content page'))

        permission = 'ftw.contentpage: Toggle IAuthority marker interface'
        page.manage_permission(permission, roles=[], acquire=False)

        roles = [r['name'] for r in page.rolesOfPermission(permission) if r[
            'selected']]
        self.assertEquals(roles,
                          [],
                          'No one should have the permission: {0}'.format(
                              permission))
