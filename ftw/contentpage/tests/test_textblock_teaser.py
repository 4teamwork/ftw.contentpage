from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from unittest import TestCase
import transaction


class TestTextblockTeaser(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):

        self.contentpage = create(Builder('content page')
                                  .titled('ContentPage'))
        self.textblock = create(Builder('text block')
                                .titled('TextBlock')
                                .having(showTitle='True',
                                        imageCaption='Image Caption',
                                        text="Lorem ipsum dolor sit amet.")
                                .with_dummy_content()
                                .within(self.contentpage))

    @browsing
    def test_image_is_not_clickable_by_default(self, browser):
        browser.open(self.contentpage)

        self.assertEquals(0,
                          len(browser.css('.textblock .sl-img-wrapper a')))

    @browsing
    def test_image_shows_colorbox_when_clickable_but_no_teaser_set(self, browser):
        self.textblock.setImageClickable(True)
        transaction.commit()
        browser.open(self.contentpage)

        img_link = browser.css('.textblock .sl-img-wrapper a').first_or_none
        self.assertTrue(img_link, "Image is does not have a link")

        self.assertEquals(img_link.attrib['href'],
                          'http://nohost/plone/contentpage/textblock/image')

    @browsing
    def test_internal_teaser(self, browser):
        linktarget = create(Builder('content page'))

        self.textblock.setTeaserSelectLink('intern')
        self.textblock.setTeaserReference(linktarget)
        transaction.commit()

        browser.open(self.textblock)
        self.assertEquals(
            'http://nohost/plone/contentpage-1',
            browser.css('.textblock .sl-img-wrapper a').first.attrib['href'])

    @browsing
    def test_external_teaser(self, browser):
        linktarget = 'http://www.google.ch'

        self.textblock.setTeaserSelectLink('extern')
        self.textblock.setTeaserExternalUrl(linktarget)
        transaction.commit()

        browser.open(self.contentpage)

        self.assertEquals(
            linktarget,
            browser.css('.textblock .sl-img-wrapper a').first.attrib['href'])

    @browsing
    def test_teaser_disables_colorbox(self, browser):
        linktarget = 'http://www.google.ch'

        # teaser takes priority over colorbox
        self.textblock.setImageClickable(True)

        self.textblock.setTeaserSelectLink('extern')
        self.textblock.setTeaserExternalUrl(linktarget)
        transaction.commit()

        browser.open(self.contentpage)

        self.assertEquals(
            ['disableColorbox'],
            browser.css('.textblock .sl-img-wrapper a').first.classes,
            "Teaser image needs marker class to not get colorboxed.")

        self.assertEquals(
            linktarget,
            browser.css('.textblock .sl-img-wrapper a').first.attrib['href'])

    @browsing
    def test_teaser_link_on_title(self, browser):
        linktarget = 'http://www.google.ch'

        browser.open(self.contentpage)
        self.assertEquals(
            0,
            len(browser.css('div.TextBlock > h2 > a')),
            "The title must not contain a link.")

        self.textblock.setTeaserSelectLink('extern')
        self.textblock.setTeaserExternalUrl(linktarget)
        transaction.commit()

        browser.open(self.contentpage)
        self.assertEquals(
            1,
            len(browser.css('div.TextBlock > h2 > a')),
            "The title should link to the teaser target."
            )

        self.assertEquals(
            'http://www.google.ch',
            browser.css('.TextBlock > h2 > a').first.attrib['href'],
            "The title must link to the teaser target.")
