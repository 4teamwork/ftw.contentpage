from ftw.contentpage import _
from plone.autoform import directives
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.annotation import AnnotationsFactoryImpl
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import alsoProvides


class IContentCategories(model.Schema):

    """Content categories schema"""

    content_categories = schema.Tuple(
        title=_(u'label_categories', default=u'Categories'),
        description=_(u'help_categories',
                      default=u'Category for contentlisting'),
        value_type=schema.Choice(title=_(u"categories"),
                                 vocabulary='ftw.contentpage.contentcategories'),
        required=False,
        missing_value=(),
    )
    directives.widget('content_categories', CheckBoxFieldWidget)

    write_permission(new_content_categories='ftw.contentpage.content_categories_behavior.add_new_categories')
    new_content_categories = schema.Tuple(
        title=_(u'label_new_categories', default=u'New categories'),
        description=_(u'help_new_categories',
                      default=u'New categories for contentlisting'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


alsoProvides(IContentCategories, IFormFieldProvider)


class ContentCategoriesStorage(object):

    def __init__(self, context):
        self.context = context
        self.annoation_storage = AnnotationsFactoryImpl(
            self.context,
            IContentCategories
        )

    @property
    def content_categories(self):
        return self.annoation_storage.content_categories

    @content_categories.setter
    def content_categories(self, value):
        self.annoation_storage.content_categories = value

    @property
    def new_content_categories(self):
        return ()

    @new_content_categories.setter
    def new_content_categories(self, value):
        if value is None:
            return ()
        else:
            categories = tuple(self.annoation_storage.content_categories)
            self.annoation_storage.content_categories = tuple(set(
                categories + value
            ))
