from ftw.testing import MockTestCase
from ftw.contentpage.vocabularies import SubjectVocabulary
from plone.i18n.normalizer.interfaces import IIDNormalizer
from mocker import ANY

TEST_SUBJECTS = ['Spam', 'and', 'eggs']


class TestVocabulary(MockTestCase):

    def setUp(self):
        super(TestVocabulary, self).setUp()
        self.context = self.stub()
        cat = self.stub()
        self.mock_tool(cat, 'portal_catalog')
        self.expect(cat.uniqueValuesFor("Subject")).result(TEST_SUBJECTS)
        normalizer = self.stub()
        self.mock_utility(normalizer, IIDNormalizer)
        self.expect(normalizer.normalize(ANY)).call(lambda term: term.lower())
        self.replay()

    def test_vocabulary(self):
        vocab = SubjectVocabulary(self.context)
        self.assertEqual(len(vocab), 3)
        for i, item in enumerate(vocab):
            self.assertTrue(isinstance(item.title, unicode))
            self.assertEqual(item.token, TEST_SUBJECTS[i].lower())
            self.assertEqual(item.value, TEST_SUBJECTS[i])
