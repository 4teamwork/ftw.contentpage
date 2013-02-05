from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.interface import directlyProvides
from Products.CMFCore.utils import getToolByName


def SubjectVocabulary(context):
    """Returns a vocabulary of the available suppliers
    """
    # context is the portal config options, whose context is the portal
    catalog = getToolByName(context, 'portal_catalog')
    terms = []
    for term in catalog.uniqueValuesFor("Subject"):
        terms.append(SimpleTerm(value=term[0], token=term[0], title=term[0]))
    return vocabulary.SimpleVocabulary(terms)

directlyProvides(SubjectVocabulary, IVocabularyFactory)
