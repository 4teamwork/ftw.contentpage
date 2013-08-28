from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class OpenlayersViewlet(ViewletBase):
    index = ViewPageTemplateFile('openlayers.pt')

    # @property
    # def is_organisation(self):
    #     '''
    #     Check if the given context is a
    #     '''
    #     if (hasattr(aq_base(self.context), 'isTemporary') and
    #             self.context.isTemporary()):
    #         # if we are in the portal_factory we want the page title to be
    #         # "Add fti title"
    #         portal_types = getToolByName(self.context, 'portal_types')
    #         fti = portal_types.getTypeInfo(self.context)
    #         return translate('heading_add_item',
    #                          domain='plone',
    #                          mapping={'itemtype': fti.Title()},
    #                          context=self.request,
    #                          default='Add ${itemtype}')

    #     context_state = getMultiAdapter((self.context, self.request),
    #                                     name=u'plone_context_state')
    #     return escape(safe_unicode(context_state.object_title()))

    # def update(self):
    #     portal_state = getMultiAdapter((self.context, self.request),
    #                                    name=u'plone_portal_state')
    #     portal_title = escape(safe_unicode(portal_state
    #                                        .navigation_root_title()))
    #     if self.page_title == portal_title:
    #         self.site_title = portal_title
    #     else:
    #         self.site_title = u"%s &mdash; %s" % (self.page_title,
    #                                               portal_title)
