from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collections import defaultdict
from plone.memoize import instance
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import unicodedata


ALPHABET = map(chr, range(ord('A'), ord('Z') + 1))
LETTERS = ALPHABET + ['#']


def normalized_first_letter(text):
    text = make_sortable(text)
    return text[0].upper()


def make_sortable(text):
    text = text.lower()
    text = text.decode('utf-8')
    normalized = unicodedata.normalize('NFKD', text)
    text = u''.join([c for c in normalized if not unicodedata.combining(c)])
    text = text.encode('utf-8')
    return text


class AlphabeticalSubjectListing(BrowserView):

    def __init__(self, *args, **kwargs):
        super(AlphabeticalSubjectListing, self).__init__(*args, **kwargs)
        self.letter = None

    def subjects(self):
        current_letter = self.get_current_letter()

        subjects = []
        for subject in self.available_subjects():

            if current_letter == '#':
                if normalized_first_letter(subject) not in ALPHABET:
                    subjects.append(subject)

            else:
                if normalized_first_letter(subject) == current_letter:
                    subjects.append(subject)

        return subjects

    def result(self):
        content = self.get_content_by_subjects(self.subjects())
        result = []

        for subject, brains in content.items():
            brains = sorted(brains,
                            key=lambda brain:make_sortable(brain.Title))
            result.append({
                    'subject': subject,
                    'brains': brains})

        return sorted(result,
                      key=lambda item: make_sortable(item['subject']))

    def get_content_by_subjects(self, subjects):
        catalog = getToolByName(self.context, 'portal_catalog')
        result = defaultdict(list)
        query = {'Subject': subjects,
                 'portal_type': self.portal_types_to_list}

        for brain in catalog(query):

            # Ignore brains without the filtered subject
            if self.ignore_brain(brain.Subject):
                continue

            for subj in brain.Subject:

                if subj not in subjects:
                    continue

                result[subj].append(brain)
        return result

    def ignore_brain(self, brain_subjects):
        if not self.subject_filter:
            return False

        if self.subject_filter in brain_subjects:
            return False
        return True

    def letters(self):
        letters_with_content = self._letters_with_content
        current_letter = self.get_current_letter()

        for letter in LETTERS:
            if letter == '#':
                character = '!'
            else:
                character = letter
            yield {'label': letter,
                   'has_contents': letter in letters_with_content,
                   'link': self.get_letter_link(character),
                   'current': letter == current_letter}

    def get_letter_link(self, character):
        link = '/'.join((self.context.absolute_url(),
                                     '@@subject-listing',
                                     character))

        if self.subject_filter:
            link = "{0}?subject_filter={1}".format(
                link,
                self.subject_filter)

        return link

    def has_contents(self):
        return bool(len(self._letters_with_content))

    def publishTraverse(self, request, name):
        if name == '!':
            self.letter = '#'
        else:
            self.letter = name
        return self

    @property
    def subject_filter(self):
        return self.request.form.get(
            'subject_filter', self.context.getProperty('subject_filter'))

    def available_subjects(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        if not self.subject_filter:
            return catalog.uniqueValuesFor("Subject")

        brains = catalog.searchResults(Subject=self.subject_filter)
        subjects = []

        for brain in brains:
            for subject in brain.Subject:

                # Exclude the filtered subjects
                if subject == self.subject_filter:
                    continue

                # Subject already exists
                if subject in subjects:
                    continue

                subjects.append(subject)

        return subjects

    def get_mimetype_icon(self, brain):
        registry = getUtility(IRegistry)
        if not registry['ftw.contentpage.subjectlisting.show_mimetype_icon']:
            return None

        icon = brain.getIcon

        if not icon:
            return None

        portal_url = getToolByName(self.context, 'portal_url')

        return '%s/%s' % (portal_url(), icon)

    @instance.memoize
    def get_current_letter(self):
        if self.letter is not None:
            return self.letter

        return self._letters_with_content[0]

    @property
    @instance.memoize
    def _letters_with_content(self):
        values = self.available_subjects()

        letters = set([])
        for subject in values:
            first_letter = normalized_first_letter(subject)
            if first_letter in ALPHABET:
                letters.add(first_letter)
            else:
                letters.add('#')

        return sorted(letters, key=LETTERS.index)

    @property
    def portal_types_to_list(self):
        registry = getUtility(IRegistry)
        return registry['ftw.contentpage.subjectlisting.portal_types']
