from zope.component import queryUtility
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.interface import directlyProvides
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName


def SubjectVocabulary(context):
    """Returns a vocabulary of the available suppliers
    """
    # context is the portal config options, whose context is the portal
    catalog = getToolByName(context, 'portal_catalog')
    normalizer = queryUtility(IIDNormalizer)
    terms = []
    for term in catalog.uniqueValuesFor("Subject"):
        terms.append(SimpleTerm(value=term,
                                token=normalizer.normalize(term),
                                title=term.decode('utf8')))
    return vocabulary.SimpleVocabulary(terms)

directlyProvides(SubjectVocabulary, IVocabularyFactory)
