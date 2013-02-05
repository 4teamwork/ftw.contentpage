from ftw.testing import MockTestCase
from ftw.contentpage.vocabularies import SubjectVocabulary

class TestVocabulary(MockTestCase):

    def setUp(self):
        super(TestVocabulary, self).setUp()
        self.context = self.stub()
        cat = self.stub()
        self.mock_tool(cat, 'portal_catalog')
        self.expect(cat.uniqueValuesFor("Subject")).result([['a'], ['b'], ['c']])
        self.replay()

    def test_vocabulary(self):
        vocab = SubjectVocabulary(self.context)
        self.assertEqual(len(vocab), 3)
        item_list = []
        for item in vocab:
            item_list.append(item.title)
        self.assertEqual(item_list[0], 'a')
        self.assertEqual(item_list[1], 'b')
        self.assertEqual(item_list[2], 'c')
