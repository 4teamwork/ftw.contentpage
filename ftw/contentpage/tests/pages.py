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
