from ftw.testing import MockTestCase
from ftw.contentpage.vocabularies import SubjectVocabulary
from plone.i18n.normalizer.interfaces import IIDNormalizer
from mocker import ANY


class TestVocabulary(MockTestCase):

    def setUp(self):
        super(TestVocabulary, self).setUp()
        self.context = self.stub()
        cat = self.stub()
        self.mock_tool(cat, 'portal_catalog')
        self.expect(cat.uniqueValuesFor("Subject")).result(['Spam', 'and', 'eggs'])
        normalizer = self.stub()
        self.mock_utility(normalizer, IIDNormalizer)
        self.expect(normalizer.normalize(ANY)).call(lambda term: term)
        self.replay()

    def test_vocabulary(self):
        vocab = SubjectVocabulary(self.context)
        self.assertEqual(len(vocab), 3)
        item_list = []
        for item in vocab:
            item_list.append(item.title)
        self.assertEqual(item_list[0], 'Spam')
        self.assertEqual(item_list[1], 'and')
        self.assertEqual(item_list[2], 'eggs')
