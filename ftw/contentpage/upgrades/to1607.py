from ftw.contentpage.portlets import news_portlet
from ftw.upgrade import UpgradeStep
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility


class UpgradeNewsPortlet(UpgradeStep):
    """Upgrade news portlets: add always_render_portlet default value to assignments.

    When news portlets were added to the Plone site before ftw.contentpage 1.9.0,
    the assignment has no always_render_portlet attribute.
    When exporting portlets with Generic Setup, the Plone site assignments are
    exported. If the attribute is missing, an AttributeError is raised.
    """

    def __call__(self):
        for assignment in self.news_portlet_assignments_for(self.portal):
            assignment.always_render_portlet = getattr(
                assignment, 'always_render_portlet', False)

    def news_portlet_assignments_for(self, context):
        for assignment in self.get_assignments_for(self.portal):
            if isinstance(assignment, news_portlet.Assignment):
                yield assignment

    def get_assignments_for(self, context):
        for manager_name in ('plone.leftcolumn', 'plone.rightcolumn'):
            manager = getUtility(IPortletManager, name=manager_name,
                                 context=self.portal)
            for assignment in getMultiAdapter((context, manager),
                                              IPortletAssignmentMapping,
                                              context=self.portal).values():
                yield assignment
