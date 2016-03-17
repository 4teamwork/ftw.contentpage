from Acquisition import IAcquirer, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.contentpage import _
from ftw.contentpage.browser.baselisting import BaseListing
from ftw.contentpage.interfaces import INewsListingView
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import implements


class NewsListing(BaseListing):
    implements(INewsListingView)

    default_template = ViewPageTemplateFile('newslisting.pt')
    rss_template = ViewPageTemplateFile('newslisting_rss.pt')

    @property
    def template(self):
        if self.__name__ == 'news_rss_listing':
            return self.rss_template
        else:
            return self.default_template

    def show_author(self):
        """Checks if the user is anonymous and is not allowAnonymousViewAbout.
        """
        site_props = getToolByName(self.context,
                                   'portal_properties').site_properties
        mt = getToolByName(self.context, 'portal_membership')

        if not site_props.getProperty('allowAnonymousViewAbout', False) \
                and mt.isAnonymousUser():
            return False
        return True

    def get_items(self):
        """Get all news items"""
        query = {}
        query['object_provides'] = 'ftw.contentpage.interfaces.INews'
        query['sort_on'] = 'effective'
        query['sort_order'] = 'reverse'

        # Implement archive functionality - used by the archive portlet
        return self.search_results(query, 'effective')

    def title(self):
        title = self.context.Title()
        if self.context.portal_type == 'NewsFolder':
            return title
        else:
            return self.context.Title() + ' - News'

    def link(self):
        return self.context.absolute_url() + '/' + self.__name__

    def description(self):
        return _(u'label_feed_desc',
                 default=u'${title} - News Feed',
                 mapping={'title': self.context.Title().decode('utf-8')})


class NewsPortletListing(NewsListing):

    def get_portlet(self):
        manager_name = self.request.form.get('manager', None)
        name = self.request.form.get('portlet', None)
        if not manager_name or not name:
            return

        managers_and_assignments = self.get_manager_and_assignments(
            manager_name
        )
        for manager, assignments in managers_and_assignments:
            if name in assignments:
                return queryMultiAdapter(
                    (self.context, self.request, self,
                     manager, assignments[name]),
                    IPortletRenderer)
        return

    def get_manager_and_assignments(self, manager_name):
        context = self.context

        # Prepare a list of objects by walking up the path.
        contexts = [context]
        while not IPloneSiteRoot.providedBy(context):
            context = aq_parent(aq_inner(context))
            contexts.append(context)

        # Prepare a list of tuples in the form `(manager, assignments)`.
        managers_and_assignments = []
        for context in contexts:
            manager = getUtility(
                IPortletManager,
                name=manager_name,
                context=context)
            assignments = getMultiAdapter(
                (context, manager),
                IPortletAssignmentMapping,
                context=context)

            if assignments is not None:
                managers_and_assignments.append((manager, assignments))

        return managers_and_assignments

    def get_items(self):
        portlet = self.get_portlet()
        if portlet:
            # Get the news items from the portlet. Tell the portlet that
            # it is the listing view who asks for the news items.
            return portlet.get_news(all_news=True, listing_view=True)

        return []

    def title(self):
        portlet = self.get_portlet()
        if portlet:
            return portlet.data.portlet_title
        return super(NewsPortletListing, self).title()
