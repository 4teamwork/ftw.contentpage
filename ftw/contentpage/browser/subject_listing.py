from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from collections import defaultdict
from plone.memoize import instance
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
        catalog = getToolByName(self.context, 'portal_catalog')
        current_letter = self.get_current_letter()

        subjects = []
        for subject in catalog.uniqueValuesFor("Subject"):
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

        for brain in catalog({'Subject': subjects}):
            for subj in brain.Subject:
                if subj not in subjects:
                    continue

                result[subj].append(brain)
        return result

    def letters(self):
        letters_with_content = self._letters_with_content
        current_letter = self.get_current_letter()

        for letter in LETTERS:
            yield {'label': letter,
                   'has_contents': letter in letters_with_content,
                   'link': '',
                   'current': letter == current_letter}

    def has_contents(self):
        return bool(len(self._letters_with_content))

    def publishTraverse(self, request, name):
        self.letter = name
        return self

    @instance.memoize
    def get_current_letter(self):
        if self.letter is not None:
            return self.letter

        return self._letters_with_content[0]

    @property
    @instance.memoize
    def _letters_with_content(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        values = catalog.uniqueValuesFor("Subject")

        letters = set([])
        for subject in values:
            first_letter = normalized_first_letter(subject)
            if first_letter in ALPHABET:
                letters.add(first_letter)
            else:
                letters.add('#')

        return sorted(letters, key=LETTERS.index)
