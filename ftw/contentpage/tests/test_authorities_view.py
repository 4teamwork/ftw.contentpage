from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.browser import authorities
from ftw.contentpage.interfaces import IOrgUnitMarker
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.contentpage.tests.pages import AuthoritiesView
from ftw.testing import MockTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase
import transaction


class TestHelperFunctions(MockTestCase):

    def setUp(self):
        super(TestHelperFunctions, self).setUp()

        self.brain_mocks = [
            self.create_dummy(Title='Foo',
                              getPath=lambda: '/plone/foo',
                              getURL=lambda: 'http://nohost/plone/foo'),

            self.create_dummy(Title='Bar',
                              getPath=lambda: '/plone/foo/bar',
                              getURL=lambda: 'http://nohost/plone/foo/bar'),

            self.create_dummy(Title='Baz',
                              getPath=lambda: '/plone/foo/baz',
                              getURL=lambda: 'http://nohost/plone/foo/baz')]

    def test_get_brain_data(self):
        self.assertEqual(map(authorities.get_brain_data, self.brain_mocks),

                         [{'title': 'Foo',
                           'path': '/plone/foo',
                           'url': 'http://nohost/plone/foo',
                           'children': []},

                          {'title': 'Bar',
                           'path': '/plone/foo/bar',
                           'url': 'http://nohost/plone/foo/bar',
                           'children': []},

                          {'title': 'Baz',
                           'path': '/plone/foo/baz',
                           'url': 'http://nohost/plone/foo/baz',
                           'children': []}])

    def test_make_treeish(self):
        data = map(authorities.get_brain_data, self.brain_mocks)

        self.maxDiff = None
        self.assertEqual(
            authorities.make_treeish(data),

            [{'title': 'Foo',
              'path': '/plone/foo',
              'url': 'http://nohost/plone/foo',

              'children': [

                        {'title': 'Bar',
                         'path': '/plone/foo/bar',
                         'url': 'http://nohost/plone/foo/bar',
                         'children': []},

                        {'title': 'Baz',
                         'path': '/plone/foo/baz',
                         'url': 'http://nohost/plone/foo/baz',
                         'children': []},

                        ]},
             ])


class TestTreeView(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_only_first_two_levels_visible(self):
        container = create(Builder('content page'))

        first = create(Builder('content page')
                       .titled('First')
                       .providing(IOrgUnitMarker)
                       .within(container))

        second = create(Builder('content page')
                        .titled('Second')
                        .providing(IOrgUnitMarker)
                        .within(first))

        create(Builder('content page')
               .titled('Third')
               .providing(IOrgUnitMarker)
               .within(second))

        AuthoritiesView().visit_on(container)
        self.assertEquals(['First', 'Second'], AuthoritiesView().link_labels)

    def test_view_has_two_columns(self):
        container = create(Builder('content page'))

        create(Builder('content page')
               .titled('One')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Two')
               .providing(IOrgUnitMarker)
               .within(container))

        AuthoritiesView().visit_on(container)
        self.assertEquals([['One'], ['Two']],
                          AuthoritiesView().link_labels_per_column)

    def test_only_pages_with_orgunit_marker_interface_are_displayed(self):
        container = create(Builder('content page'))

        create(Builder('content page')
               .titled('With IOrgUnitMarker')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Without IOrgUnitMarker')
               .within(container))

        AuthoritiesView().visit_on(container)
        self.assertEquals(['With IOrgUnitMarker'],
                          AuthoritiesView().link_labels)

    def test_pages_are_linked_properly(self):
        container = create(Builder('content page'))

        foo = create(Builder('content page')
                     .titled('Foo')
                     .providing(IOrgUnitMarker)
                     .within(container))

        bar = create(Builder('content page')
                     .titled('Bar')
                     .providing(IOrgUnitMarker)
                     .within(container))

        AuthoritiesView().visit_on(container)
        self.assertEquals(
            [foo.absolute_url(),
             bar.absolute_url()],

            [AuthoritiesView().link_url('Foo'),
             AuthoritiesView().link_url('Bar')])

    def test_column_balancing_can_be_changed_with_property(self):
        container = create(Builder('content page'))

        create(Builder('content page')
               .titled('One')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Two')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Three')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Four')
               .providing(IOrgUnitMarker)
               .within(container))

        AuthoritiesView().visit_on(container)
        self.assertEquals([['One', 'Two'],
                           ['Three', 'Four']],
                          AuthoritiesView().link_labels_per_column)

        container._setProperty('leftcolumn_num_elements', 1, 'int')
        transaction.commit()
        AuthoritiesView().visit_on(container)
        self.assertEquals([['One'],
                           ['Two', 'Three', 'Four']],
                          AuthoritiesView().link_labels_per_column)

    def test_pages_excluded_from_navigation_are_not_shown(self):
        container = create(Builder('content page'))

        create(Builder('content page')
               .titled('Shown In Navigation')
               .providing(IOrgUnitMarker)
               .within(container))

        create(Builder('content page')
               .titled('Excluded From Navigation')
               .providing(IOrgUnitMarker)
               .within(container)
               .having(excludeFromNav=True))

        AuthoritiesView().visit_on(container)
        self.assertEquals(['Shown In Navigation'],
                          AuthoritiesView().link_labels)
