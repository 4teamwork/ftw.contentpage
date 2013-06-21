from Acquisition import aq_parent, aq_inner
from DateTime import DateTime
from ftw.contentpage import _
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.portlets import base
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import form, button, field, interfaces
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements, invariant, Invalid


class INewsPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=u'',
        required=True,
        default=u'')

    show_image = schema.Bool(title=_(u'label_show_image'),
                             required=True,
                             default=True)

    path = schema.List(
        title=_(u"Path"),
        description=u"",
        value_type=schema.Choice(
            source=PathSourceBinder(
                navigation_tree_query={
                    'is_folderish': True},
                is_folderish=True),
        ),
        required=False,
    )

    only_context = schema.Bool(title=_(u'label_only_context'),
                               description=_('help_only_context'),
                               default=True,
                               )

    classification_items = schema.List(
        title=_(u"Classification Items"),
        description=u"",
        value_type=schema.Choice(
            source=PathSourceBinder(
                navigation_tree_query={
                    'portal_type': 'ClassificationItem'},
                portal_type='ClassificationItem'),
        ),
        required=False,
    )

    quantity = schema.Int(title=_(u'label_quantity'),
                          default=5)

    subjects = schema.List(
        title=_(u'label_subjects'),
        value_type=schema.Choice(
            vocabulary='ftw.contentpage.subjects',

        ),
        required=False
    )

    show_desc = schema.Bool(title=_(u'label_show_desc',
                                    default=u"Show Description"),
                            default=True)

    desc_length = schema.Int(title=_(u'label_desc_length'),
                             default=50)

    days = schema.Int(title=_(u'label_days', default="Days"),
                      description=_(u'description_days',
                                    default="Show news of the las x days."),
                      default=0,
                      required=True)

    more_news_link = schema.Bool(title=_(u'label_more_news_link',
                                    default=u"Show more news link"),
                            default=False)

    @invariant
    def is_either_path_or_area(obj):
        """Checks if not both path and current area are defined.
        """
        if obj.only_context and obj.path:
            raise Invalid(
                _(u'text_path_and_area',
                  default=u'You can not set a path and limit to context.'))


class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label = _(u'Add News Portlet')
    description = _(u'This Portlet displays News')

    fields = field.Fields(INewsPortlet)

    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self.status = None
        self._finishedAdd = None

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    def add(self, object_):
        ob = self.context.add(object_)
        self._finishedAdd = True
        return ob

    def updateWidgets(self):
        self.fields['classification_items'].widgetFactory = \
            MultiContentTreeFieldWidget
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        if not self.context.portal_types.get('ClassificationItem', None):
            self.fields['classification_items'].mode = interfaces.HIDDEN_MODE
        else:
            self.fields['classification_items'].mode = interfaces.INPUT_MODE
        super(AddForm, self).updateWidgets()

    def create(self, data):
        return Assignment(
            portlet_title=data.get('portlet_title', 'News'),
            show_image=data.get('show_image', True),
            only_context=data.get('only_context', True),
            quantity=data.get('quantity', 5),
            classification_items=data.get('classification_items', []),
            path=data.get('path', []),
            subjects=data.get('subjects', []),
            show_desc=data.get('show_desc', False),
            desc_length=data.get('desc_length', 50),
            days=data.get('days', 0),
            more_news_link=data.get('more_news_link', 0)
        )


class Assignment(base.Assignment):
    implements(INewsPortlet)

    def __init__(self, portlet_title="News", show_image=True,
                 only_context=True, quantity=5, classification_items=None,
                 path=None, subjects=None, show_desc=False, desc_length=50,
                 days=0, more_news_link=0):
        self.portlet_title = portlet_title
        self.show_image = show_image
        self.only_context = only_context
        self.quantity = quantity
        self.classification_items = classification_items or []
        self.path = path or []
        self.subjects = subjects or []
        self.show_desc = show_desc
        self.desc_length = desc_length
        self.days = days
        self.more_news_link = more_news_link

    @property
    def title(self):
        return u'News Portlet'


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('news_portlet.pt')

    def tag_image(self, brain):
        if not self.data.show_image:
            return ''
        obj = brain.getObject()
        scale = getMultiAdapter((obj, self.request), name=u"images")
        scaled_img = scale.scale('image', scale='thumb', direction='down')

        if scaled_img:
            return scaled_img.tag()
        return ''

    @property
    def available(self):
        is_news = self.context.portal_type in ['News', 'NewsFolder']
        if self.show_more_news_link():
            has_news = self.get_news(all_news=True)
        else:
            has_news = self.get_news()
        return has_news and not is_news

    def get_news(self, all_news=False):
        catalog = getToolByName(self.context, 'portal_catalog')
        url_tool = getToolByName(self.context, 'portal_url')
        portal_path = url_tool.getPortalPath()
        query = {'object_provides': 'ftw.contentpage.interfaces.INews'}

        if self.data.only_context:
            path = '/'.join(self.context.getPhysicalPath())
            query['path'] = {'query': path}

        else:
            if self.data.path:
                cat_path = []
                for item in self.data.path:
                    cat_path.append('/'.join([portal_path, item]))
                query['path'] = {'query': cat_path}

        if self.data.classification_items:
            cs_uids = []
            for item in self.data.classification_items:
                obj = self.context.restrictedTraverse(
                    '/'.join([portal_path, item.strip('/')]))
                cs_uids.append(obj.UID())
            query['cs_uids'] = cs_uids

        if self.data.subjects:
            query['Subject'] = self.data.subjects

        if self.data.days > 0 and not all_news:
            date = DateTime() - self.data.days
            query['effective'] = {'query': date, 'range': 'min'}

        query['sort_on'] = 'effective'
        query['sort_order'] = 'descending'
        results = catalog.searchResults(query)
        return results[:self.data.quantity]

    def crop_desc(self, description):
        ploneview = self.context.restrictedTraverse('@@plone')
        return ploneview.cropText(description, self.data.desc_length)

    def show_more_news_link(self):
        return self.data.more_news_link


class EditForm(form.EditForm):
    implements(IPortletEditForm)
    label = _(u'Add News Portlet')
    description = _(u'This Portlet displays News')

    fields = field.Fields(INewsPortlet)

    def __init__(self, context, request):
        super(EditForm, self).__init__(context, request)
        self.status = None
        self._finishedAdd = None

    def __call__(self):
        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(EditForm, self).__call__()

    def nextURL(self):
        editview = aq_parent(aq_inner(self.context))
        context = aq_parent(aq_inner(editview))
        url = str(getMultiAdapter((context, self.request),
                                  name=u"absolute_url"))
        return url + '/@@manage-portlets'

    @button.buttonAndHandler(_(u"label_save", default=u"Save"), name='apply')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    @button.buttonAndHandler(_(u"label_cancel", default=u"Cancel"),
                             name='cancel_add')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)

    def updateWidgets(self):
        self.fields['classification_items'].widgetFactory = \
            MultiContentTreeFieldWidget
        self.fields['path'].widgetFactory = MultiContentTreeFieldWidget
        if not self.context.portal_types.get('ClassificationItem', None):
            self.fields['classification_items'].mode = interfaces.HIDDEN_MODE

        super(EditForm, self).updateWidgets()
