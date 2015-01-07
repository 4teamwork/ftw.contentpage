from Acquisition import aq_inner
from email.header import Header
from email.mime.text import MIMEText
from ftw.contentpage import _
from plone import api
from plone.formwidget.recaptcha.widget import ReCaptchaFieldWidget
from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, field, button
from z3c.form.interfaces import WidgetActionExecutionError
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import Invalid
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
    captcha = schema.TextLine(title=u"ReCaptcha",
                              required=False)


class FeedbackForm(form.Form):
    label = _(u"label_send_feedback", default=u"Send Feedback")
    fields = field.Fields(IFeedbackView)

    # don't use context to get widget data
    ignoreContext = True

    def updateWidgets(self):
        captcha_enabled = self.recaptcha_enabled()
        if captcha_enabled:
            self.fields['captcha'].widgetFactory = ReCaptchaFieldWidget

        super(FeedbackForm, self).updateWidgets()

        if not captcha_enabled:
            # Simply delete the widget instead of trying to set hidden mode,
            # which caused a `ComponentLookupError` in a special case. Please
            # see `test_captcha_no_component_lookup_error`.
            del self.widgets['captcha']

    def recaptcha_enabled(self):
        registry = getUtility(IRegistry, context=self)
        private_key = registry.get(
            'plone.formwidget.recaptcha.interfaces.'
            'IReCaptchaSettings.private_key',
            u'')
        public_key = registry.get(
            'plone.formwidget.recaptcha.interfaces.'
            'IReCaptchaSettings.public_key',
            u'')
        return (public_key and private_key and api.user.is_anonymous())

    @button.buttonAndHandler(_(u'Send Mail'))
    def handleApply(self, action):
        data, errors = self.extractData()

        if self.recaptcha_enabled():
            captcha = getMultiAdapter((aq_inner(self.context), self.request),
                                      name='recaptcha')
            if not captcha.verify():
                raise WidgetActionExecutionError(
                    'captcha',
                    Invalid(_("The captcha code you entered was wrong, "
                              "please enter the new one.")))

        if errors:
            return

        message = data.get('message')
        email = data.get('email')
        subject = data.get('subject')
        sender = data.get('sender').replace(',', ' ')
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
        msg = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        msg['From'] = Header('%s' % portal.getProperty('email_from_name'),
                             'utf-8')
        msg['From'].append(
            "<%s>" % portal.getProperty('email_from_address').decode('utf-8'))
        if isinstance(sender, unicode):
            sender = sender.encode('utf-8')
        msg['Reply-To'] = Header("%s" % sender, 'utf-8')
        msg['Reply-To'].append("<%s>" % recipient)
        msg['To'] = self.context.getEmail()
        # send the message
        mh.send(msg)


FeedbackView = wrap_form(FeedbackForm)
