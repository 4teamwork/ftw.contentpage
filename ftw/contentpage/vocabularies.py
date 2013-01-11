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
    subject_index = None
    for index in catalog.getIndexObjects():
        if index.id == "Subject":
            subject_index = index
    for item in subject_index.items():
        terms.append(SimpleTerm(value=item[0], token=item[0], title=item[0]))
    return vocabulary.SimpleVocabulary(terms)

directlyProvides(SubjectVocabulary, IVocabularyFactory)
