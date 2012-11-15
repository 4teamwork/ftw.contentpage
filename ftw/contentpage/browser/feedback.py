from email.header import Header
from email.mime.text import MIMEText
from ftw.contentpage import _
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, field, button
from zope import schema
from zope.i18n import translate
from zope.interface import Interface
import re


def is_email(value):
    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +
                      r"?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +
                      r"\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$",
                      re.IGNORECASE)

    return bool(expr.match(value))


class IFeedbackView(Interface):
    """Interface for z3c.form"""
    sender = schema.TextLine(title=_(u"Sender_Name", default=u"Name"),
                             required=True)
    email = schema.TextLine(title=_(u"mail_address", default="E-Mail"),
                            required=True,
                            constraint=is_email)
    subject = schema.TextLine(title=_(u"label_subject", default="Subject"),
                              required=True)
    message = schema.Text(title=_(u"label_message", default="Message"),
                          required=True)


class FeedbackForm(form.Form):
    label = _(u"label_send_feedback", default=u"Send Feedback")
    fields = field.Fields(IFeedbackView)
     # don't use context to get widget data
    ignoreContext = True

    @button.buttonAndHandler(_(u'Send Mail'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return

        message = data.get('message')
        email = data.get('email')
        subject = data.get('subject')
        sender = data.get('sender')
        self.send_feedback(email, subject, message, sender)
        msg = _(u'info_email_sent', default=u'The email was sent.')
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        return self.redirect()

    @button.buttonAndHandler(_(u'button_cancel', default=u'Cancel'))
    def handle_cancel(self, action):
        return self.redirect()

    def redirect(self):
        """Redirect back
        """
        url = self.context.aq_parent.absolute_url()
        return self.request.RESPONSE.redirect(url)

    def send_feedback(self, recipient, subject, message, sender):
        """Send a feedback email to the email address defined in
        the addressblock.
        """
        mh = getToolByName(self.context, 'MailHost')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        text = translate(
            u'feedback_mail_text',
            domain='ftw.contentpage',
            default='${sender} sends you a message:\n${msg}',
            context=self.request,
            mapping={'sender': "%s (%s)" % (sender, recipient),
                     'msg': message})

        # create the message root with from, to, and subject headers
        msg = MIMEText(text.encode('windows-1252'), 'plain', 'windows-1252')
        msg['Subject'] = Header(subject, 'windows-1252')

        msg['From'] = "%s <%s>" % (
            portal.getProperty('email_from_name', ''),
            portal.getProperty('email_from_address', ''))

        msg['reply-to'] = "%s <%s>" % (sender, recipient)
        msg['To'] = self.context.getEmail()

        # send the message
        mh.send(msg, mto=self.context.getEmail(),
                mfrom=[portal.getProperty('email_from_address', '')])


FeedbackView = wrap_form(FeedbackForm)
