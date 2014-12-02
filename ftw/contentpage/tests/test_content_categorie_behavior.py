from ftw.builder import Builder
from ftw.builder import create
from ftw.builder import registry
from ftw.builder.dexterity import DexterityBuilder
from ftw.contentpage.behaviors.content_categories import IContentCategories
from ftw.contentpage.testing import FTW_CONTENTPAGE_INTEGRATION_TESTING
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface


class ISampleDX(Interface):
    title = schema.TextLine(
        title=u'Title',
        required=False)

alsoProvides(ISampleDX, IFormFieldProvider)


class SampleBuilder(DexterityBuilder):
    portal_type = 'Sample'

registry.builder_registry.register('sample', SampleBuilder)


class TestContentCategoriesBehavior(TestCase):

    layer = FTW_CONTENTPAGE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # add sample fti
        self.fti = DexterityFTI('Sample')
        self.fti.schema = 'ftw.contentpage.tests.test_content_categorie_behavior.ISampleDX'
        self.fti.behaviors = (
            'ftw.contentpage.behaviors.content_categories.IContentCategories', )

        self.portal.portal_types._setObject('Sample', self.fti)

    def test_category_index(self):
        catalog = getToolByName(self.portal, 'portal_catalog')

        create(Builder('sample')
               .having(content_categories=(u'DEMO1', )))

        self.assertTrue(catalog({'getContentCategories': 'DEMO1'})[0])

    def test_category_index_umlauts(self):
        catalog = getToolByName(self.portal, 'portal_catalog')

        create(Builder('sample')
               .having(content_categories=(u'WITH unicode \xe4', )))

        unique_values = catalog.Indexes['getContentCategories'].uniqueValues()
        self.assertIn("WITH unicode \xc3\xa4", unique_values)
