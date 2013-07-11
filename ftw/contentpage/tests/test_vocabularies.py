from ftw.testing import MockTestCase
from ftw.contentpage.vocabularies import SubjectVocabulary
from plone.i18n.normalizer.interfaces import IIDNormalizer
from mocker import ANY


class TestVocabulary(MockTestCase):

    def setUp(self):
        super(TestVocabulary, self).setUp()
        self.context = self.stub()
        self.cat = self.stub()
        self.mock_tool(self.cat, 'portal_catalog')
        normalizer = self.stub()
        self.mock_utility(normalizer, IIDNormalizer)
        self.expect(normalizer.normalize(ANY)).call(lambda term: term.lower())

    def set_subjects(self, subjects=[]):
        self.expect(self.cat.uniqueValuesFor("Subject")).result(subjects)
        self.replay()

    def test_vocabulary_needs_titles_in_unicode(self):
        self.set_subjects(['J\xc3\xa4m', 'Cheese'])

        self.assertEqual(
            [u'J\xe4m', u'Cheese'],
            [item.title for item in SubjectVocabulary(self.context)]
        )

    def test_vocabulary_values(self):
        self.set_subjects(['J\xc3\xa4m', 'Cheese'])

        self.assertEqual(
            ['J\xc3\xa4m', 'Cheese'],
            [item.value for item in SubjectVocabulary(self.context)]
        )

    def test_vocabulary_needs_unique_tokens(self):
        self.set_subjects(['Cheese', 'CHEESE'])

        self.assertEquals(
            [
            'a67778b3dcc82bfaace0f8bc0061f20e-cheese',
            '0b2ebce559f2697d6be386d52840f087-cheese',
            ],
            [item.token for item in SubjectVocabulary(self.context)]
        )
