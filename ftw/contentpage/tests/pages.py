from ftw.testing import browser
from ftw.testing.pages import Plone

INDEX_XPATH = '//*[contains(concat(" ", normalize-space(@class), " "), ' + \
    '" letter-index ")]'


class SubjectListingView(Plone):

    def visit(self):
        self.visit_portal('@@subject-listing')
        self.assert_body_class('template-subject-listing')
        return self

    @property
    def current_letter(self):
        return map(self._item_to_text,
                   browser().find_by_css('.letter-index .current'))[0]

    @property
    def linked_letters(self):
        return map(self._item_to_text,
                   browser().find_by_css('.letter-index a'))

    @property
    def mimetype_images(self):
        return browser().find_by_css('.subject-mimetype-icon')

    def click_letter(self, letter):
        xpath = INDEX_XPATH + '//a[normalize-space(text())="%s"]' % letter
        elements = browser().find_by_xpath(xpath)
        if len(elements) == 0:
            raise Exception('Letter-link for "%s" not found' % letter)
        elements.click()

    @property
    def subjects(self):
        subjects = browser().find_by_css('.subject')
        return map(self._item_to_text, subjects)

    def get_links_for(self, subject, text_only=False):
        links = browser().find_by_xpath(
            '//td[normalize-space(text())="%s"]/..//a' % subject)

        if text_only:
            return map(self._item_to_text, links)
        else:
            return links

    def _item_to_text(self, item):
        return self.normalize_whitespace(item.text.strip())

    def visit_with_subject_filter(self, value):
        self.visit_portal('@@subject-listing?subject_filter={0}'.format(value))
        self.assert_body_class('template-subject-listing')
        return self


class AuthoritiesView(Plone):

    def visit_on(self, page):
        return self.visit(page, 'authorities_view')

    @property
    def link_labels(self):
        return map(self._item_to_text, browser().find_by_css('#authorities a'))

    @property
    def link_labels_per_column(self):
        columns = []
        for column in browser().find_by_css('#authorities .listing-column'):
            columns.append(map(self._item_to_text,
                               column.find_by_css('a')))
        return columns

    def link_url(self, label):
        links = browser().find_by_xpath(
            '//*[@id="authorities"]//a[normalize-space(text())="%s"]' % label.strip())

        assert len(links) > 0, 'Link with text "%s" not found' % label.strip()
        assert len(links) == 1, 'More than one link with text "%s" found' % (
            label.strip())

        return links[0]['href']

    def _item_to_text(self, item):
        return self.normalize_whitespace(item.text.strip())
