from plone.app.layout.viewlets import content
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter


class NewsByline(content.DocumentBylineViewlet):

    template = ViewPageTemplateFile('byline.pt')

    def render(self):
        return self.template()

    def creator(self):
        userid = self.context.Creator()
        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getMemberById(userid)
        if member:
            return member.getProperty('fullname') or userid
        return userid

    def getWorkflowState(self):
        state = self.context_state.workflow_state()
        plone_tools = getMultiAdapter(
            (self.context, self.request),
            name='plone_tools')

        workflows = plone_tools.workflow().getWorkflowsFor(self.context)
        if workflows:
            for w in workflows:
                if state in w.states:
                    return w.states[state].title or state
