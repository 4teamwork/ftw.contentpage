from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.browser.subject_listing import make_sortable
from ftw.contentpage.browser.subject_listing import normalized_first_letter
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.contentpage.tests.pages import SubjectListingView
from ftw.testing import browser
from unittest2 import TestCase


class TestNormalizedFirstLetter(TestCase):

    def test_returns_uppercase_letter(self):
        self.assertEquals('T', normalized_first_letter('test'))

    def test_normalizes_umlauts(self):
        self.assertEquals('A', normalized_first_letter('\xc3\xa4bc'))


class TestMakeSortable(TestCase):

    def test_text_is_lowercased(self):
        self.assertEquals('foo',
                          make_sortable('FoO'))

    def test_umlauts_are_normalized(self):
        self.assertEquals('loffel',
                          make_sortable('L\xc3\xb6ffel'))

    def test_cedillas_are_removed(self):
        self.assertEquals('francais',
                          make_sortable('fran\xc3\xa7ais'))


class TestAlphabeticalSubjectListing(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def test_subjects_are_ordered_alphabetically(self):
        create(Builder('content page')
               .having(subject=['Airport']))

        create(Builder('content page')
               .having(subject=['Address modification',
                                'AZ']))

        view = SubjectListingView().visit()
        self.assertEquals(['Address modification', 'Airport', 'AZ'],
                          view.subjects)

    def test_subjects_with_umlauts_are_ordered_correctly(self):
        create(Builder('content page')
               .having(subject=['Grippe',
                                'Gr\xc3\xa4ber']))

        view = SubjectListingView().visit()
        self.assertEquals(['Gr\xc3\xa4ber'.decode('utf-8'),
                           'Grippe'.decode('utf-8')],
                          view.subjects)

    def test_content_links_are_ordered_alphabetically(self):
        create(Builder('content page')
               .titled('Foo')
               .having(subject=['Airport']))
        create(Builder('content page')
               .titled('Bar')
               .having(subject=['Airport']))
        create(Builder('content page')
               .titled('BAZ')
               .having(subject=['Airport']))

        view = SubjectListingView().visit()
        self.assertEquals(['Bar', 'BAZ', 'Foo'],
                          view.get_links_for('Airport', text_only=True))

    def test_content_links_with_umlauts_are_ordered_correctly(self):
        create(Builder('content page')
               .titled('G\xc3\xa4rtnerei')
               .having(subject=['Garten']))

        create(Builder('content page')
               .titled('Gr\xc3\xbcnfl\xc3\xa4chen')
               .having(subject=['Garten']))

        view = SubjectListingView().visit()
        self.assertEquals(['G\xc3\xa4rtnerei'.decode('utf-8'),
                           'Gr\xc3\xbcnfl\xc3\xa4chen'.decode('utf-8')],
                          view.get_links_for('Garten', text_only=True))

    def test_content_is_properly_linked(self):
        page = create(Builder('content page')
                      .having(subject=['Airport']))

        view = SubjectListingView().visit()
        view.get_links_for('Airport').first.click()
        self.assertEquals(page.absolute_url(), browser().url)

    def test_first_letter_with_content_is_selected(self):
        create(Builder('content page')
               .having(subject=['building application', 'crafting', '3D']))

        view = SubjectListingView().visit()
        self.assertEquals('B', view.current_letter)

    def test_only_letters_with_content_are_linked(self):
        create(Builder('content page')
               .having(subject=['building application',
                                'crafting',
                                'manufactoring']))

        view = SubjectListingView().visit()
        self.assertEquals(['B', 'C', 'M'], view.linked_letters)

    def test_navigating_in_letter_index(self):
        create(Builder('content page')
               .having(subject=['building application',
                                'crafting',
                                'manufactoring']))
        view = SubjectListingView().visit()

        self.assertEquals('B', view.current_letter)
        view.click_letter('C')
        self.assertEquals('C', view.current_letter)

    def test_only_content_of_current_is_listed(self):
        create(Builder('content page')
               .having(subject=['building application',
                                'budget',
                                'crafting']))

        create(Builder('content page')
               .having(subject=['crafting']))

        view = SubjectListingView().visit()
        self.assertEquals('B', view.current_letter)
        self.assertEquals(['budget', 'building application'],
                          view.subjects)

        view.click_letter('C')
        self.assertEquals(['crafting'],
                          view.subjects)

    def test_umlauts_are_normalized_for_letter_index(self):
        create(Builder('content page')
               .having(subject=['\xc3\xa4bc']))

        view = SubjectListingView().visit()
        self.assertEquals('A', view.current_letter)
        self.assertEquals([u'\xe4bc'], view.subjects)

    def test_non_alphabetic_subjects_are_listed_under_number_sign(self):
        create(Builder('content page')
               .having(subject=['3D',
                                '_X']))

        view = SubjectListingView().visit()
        view.click_letter('#')
        self.assertEquals(['3D', '_X'], view.subjects)

    def test_visiting_page_with_no_contents_does_not_crash(self):
        SubjectListingView().visit()

        self.assertEquals(
            'There is no content to list.',
            browser().find_by_css('#content .no-contents').text.strip())
