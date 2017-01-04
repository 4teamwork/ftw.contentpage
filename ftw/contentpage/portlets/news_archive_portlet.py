from Acquisition._Acquisition import aq_inner
from Acquisition._Acquisition import aq_parent
from ftw.contentpage import _
from ftw.contentpage.interfaces import INewsListingView
from ftw.contentpage.portlets.base_archive_portlet import ArchiveSummary
from plone.app.portlets.browser.interfaces import IPortletAddForm
from plone.app.portlets.browser.interfaces import IPortletEditForm
from plone.app.portlets.interfaces import IPortletPermissionChecker
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import form, button, field
from zope import schema
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import implements


class INewsArchivePortlet(IPortletDataProvider):
    """Archive portlet interface.
    """
    portlet_title = schema.TextLine(
        title=_(u'news_archive_portlet_title_label', default=u'Title'),
        description=_(u'news_archive_portlet_title_description',
                      default=u'Use this to override the title of the portlet.'),
        required=False,
        default=u''
    )


class Assignment(base.Assignment):
    implements(INewsArchivePortlet)

    def __init__(self, portlet_title=''):
        self.portlet_title = portlet_title

    @property
    def title(self):
        return "News Archive Portlet"


class Renderer(base.Renderer):
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.data = data
        self.request = request
        self.view = view

    @property
    def available(self):
        """Only show the portlet:
        - If there are News
        - If view is NewsListing
        """
        has_news = bool(self.archive_summary())

        if INewsListingView.providedBy(self.view):
            return has_news
        else:
            return False

    @memoize
    def archive_summary(self):
        """Returns an ordered list of summary infos per month."""
        return ArchiveSummary(
            self.context,
            self.request,
            ['ftw.contentpage.interfaces.INews'],
            'effective',
            'newslisting')()

    def get_portlet_title(self):
        default_title = translate(_(u'Archive'), context=self.request)
        return getattr(self.data, 'portlet_title', '') or default_title

    render = ViewPageTemplateFile('news_archive_portlet.pt')


class AddForm(form.AddForm):
    implements(IPortletAddForm)
    label = _(u'news_archive_portlet_add_form_label',
              default=u'Add News Archive Portlet')
    description = _(u'news_archive_portlet_add_form_description',
                    default=u'Renders a widget containing the number of news by year and month.')

    fields = field.Fields(INewsArchivePortlet)

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

    def create(self, data):
        return Assignment(
            portlet_title=data.get('portlet_title', ''),
        )


class EditForm(form.EditForm):
    implements(IPortletEditForm)
    label = _(u'news_archive_portlet_edit_form_label',
              default=u'Edit News Archive Portlet')
    description = _(u'newst_archive_portlet_edit_form_description',
                    default=u'Renders a widget containing the number of news by year and month.')

    fields = field.Fields(INewsArchivePortlet)

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
                             name='cancel_edit')
    def handleCancel(self, action):
        nextURL = self.nextURL()
        return self.request.response.redirect(nextURL)
