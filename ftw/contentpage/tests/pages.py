from ftw.testbrowser import browser as default_browser
from plone import api

INDEX_XPATH = '//*[contains(concat(" ", normalize-space(@class), " "), ' + \
    '" letter-index ")]'


class SubjectListingView(object):
    
    def __init__(self, browser=default_browser):
        self.browser = browser
        self.portal = api.portal.get()

    def visit(self):
        self.browser.visit(self.portal, view='@@subject-listing')
        assert 'template-subject-listing' in self.browser.css('body').first.classes, \
            'Expected class is not available on the body-tag'
        return self

    @property
    def current_letter(self):
        return map(self._item_to_text,
                   self.browser.css('.letter-index .current'))[0]

    @property
    def linked_letters(self):
        return map(self._item_to_text,
                   self.browser.css('.letter-index a'))

    @property
    def mimetype_images(self):
        return self.browser.css('.subject-mimetype-icon')

    def click_letter(self, letter):
        xpath = INDEX_XPATH + '//a[normalize-space(text())="%s"]' % letter
        elements = self.browser.xpath(xpath)
        if len(elements) == 0:
            raise Exception('Letter-link for "%s" not found' % letter)
        elements.first.click()

    @property
    def subjects(self):
        subjects = self.browser.css('.subject')
        return map(self._item_to_text, subjects)

    def get_links_for(self, subject, text_only=False):
        links = self.browser.xpath(
            '//td[normalize-space(text())="%s"]/..//a' % subject)

        if text_only:
            return map(self._item_to_text, links)
        else:
            return links

    def _item_to_text(self, item):
        return item.text

    def visit_with_subject_filter(self, value):
        self.browser.visit(self.portal.absolute_url() + '/@@subject-listing?subject_filter={0}'.format(value))
        assert 'template-subject-listing' in self.browser.css('body').first.classes, \
            'Expected class is not available on the body-tag'
        return self


class AuthoritiesView(object):
    
    def __init__(self, browser=default_browser):
        self.browser = browser

    def visit_on(self, page):
        return self.browser.visit(page, view='authorities_view')

    @property
    def link_labels(self):
        return map(self._item_to_text, self.browser.css('#authorities a'))

    @property
    def link_labels_per_column(self):
        columns = []
        for column in self.browser.css('#authorities .listing-column'):
            columns.append(map(self._item_to_text,
                               column.css('a')))
        return columns

    def link_url(self, label):
        links = self.browser.xpath(
            '//*[@id="authorities"]//a[normalize-space(text())="%s"]' % label.strip())

        assert len(links) > 0, 'Link with text "%s" not found' % label.strip()
        assert len(links) == 1, 'More than one link with text "%s" found' % (
            label.strip())

        return links.first.attrib['href']

    def _item_to_text(self, item):
        return item.text
