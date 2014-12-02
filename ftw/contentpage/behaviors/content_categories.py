from ftw.contentpage import _
from plone.directives import form
from zope import schema
from zope.interface import alsoProvides


class IContentCategories(form.Schema):

    """Content categories schema"""

    content_categories = schema.Tuple(
        title=_(u'label_categories', default=u'Categories'),
        description=_(u'help_categories',
                      default=u'Category for contentlisting'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


alsoProvides(IContentCategories, form.IFormFieldProvider)
