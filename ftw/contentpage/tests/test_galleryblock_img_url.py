from ftw.builder import Builder
from ftw.builder import create
from ftw.colorbox.interfaces import IColorboxSettings
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.registry.interfaces import IRegistry
from unittest2 import TestCase
from zope.component import getUtility
import transaction


class TestListingBlockCreation(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestListingBlockCreation, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        registry = getUtility(IRegistry)
        self.colorbox_settings = registry.forInterface(IColorboxSettings)

        self.page = create(Builder('content page'))
        self.listingblock = create(Builder('listing block').within(self.page))
        self.image = create(Builder('image')
                            .with_dummy_content()
                            .within(self.listingblock))

    @browsing
    def test_use_scale_for_large_image(self, browser):
        self.colorbox_settings.image_size = u'colorbox'
        transaction.commit()

        browser.login().visit(self.listingblock, view='block_view-gallery')
        link = browser.css('.sl-img-wrapper a').first

        self.assertEquals(self.get_scaled_img_url(), link.attrib['href'])

    @browsing
    def test_not_scale_defined_returns_origin_image(self, browser):
        self.colorbox_settings.image_size = u''
        transaction.commit()

        browser.login().visit(self.listingblock, view='block_view-gallery')
        link = browser.css('.sl-img-wrapper a').first

        self.assertEquals(self.image.absolute_url(), link.attrib['href'])

    @browsing
    def test_broken_scale_returns_origin_image(self, browser):
        self.colorbox_settings.image_size = u'inexisting'
        transaction.commit()

        browser.login().visit(self.listingblock, view='block_view-gallery')
        link = browser.css('.sl-img-wrapper a').first

        self.assertEquals(self.image.absolute_url(), link.attrib['href'])

    def get_scaled_img_url(self):
        scales = self.image.restrictedTraverse('@@images')
        scaled = scales.scale('image', scale=self.colorbox_settings.image_size)
        return scaled.url
