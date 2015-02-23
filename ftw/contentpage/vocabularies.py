from hashlib import md5
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.interface import directlyProvides
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


def SubjectVocabulary(context):
    """Returns a vocabulary of the available suppliers
    """
    # context is the portal config options, whose context is the portal
    catalog = getToolByName(context, 'portal_catalog')
    normalizer = queryUtility(IIDNormalizer)
    terms = []

    for term in catalog.uniqueValuesFor("Subject"):
        # Just the normalized term is not enought for an unique token.
        # The unique values are case sensitive. After normalizing the term,
        # we get id's in lower-case. That means, we lose the unique value after
        # normalizing if we get values like: "Bond" and "bonD". Adding an md5
        # hash to the normalized term, we prevent double tokens and the
        # token is still readable.
        token = '%s-%s' % (md5(term).hexdigest(), normalizer.normalize(term))
        terms.append(SimpleTerm(value=term,
                                token=token,
                                title=term.decode('utf8')))

    return vocabulary.SimpleVocabulary(terms)

directlyProvides(SubjectVocabulary, IVocabularyFactory)


def contentcategories_vocabulary(context):
    normalizer = queryUtility(IIDNormalizer)
    catalog = getToolByName(context, 'portal_catalog')
    terms = []
    for term in catalog.uniqueValuesFor("getContentCategories"):
        terms.append(SimpleTerm(value=term.decode('utf8'),
                                token=normalizer.normalize(term.decode('utf8')),
                                title=term.decode('utf8')))
    return vocabulary.SimpleVocabulary(terms)

directlyProvides(contentcategories_vocabulary, IVocabularyFactory)
