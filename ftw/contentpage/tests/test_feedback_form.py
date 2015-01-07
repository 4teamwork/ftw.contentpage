from ftw.builder import Builder
from ftw.builder import create
from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from ftw.testing import MockTestCase
from mocker import ARGS, KWARGS
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from unittest2 import TestCase
from zope.component import getUtility
import transaction


FORM_DATA = {'sender': 'Zaph\xc3\xb6d Beeblebrox',
             'email': 'z.beeblebrox@endofworld.com',
             'subject': 'Don\'t p\xc3\xa4nic',
             'message': '42'}


class TestFeedbackForm(MockTestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestFeedbackForm, self).setUp()
        self.portal = self.layer['portal']
        self.portal_url = self.portal.portal_url()

        self.contentpage = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'contentpage'))
        # Fire all necessary events
        self.contentpage.processForm()
        self.addressblock = self.contentpage.get(
            self.contentpage.invokeFactory('AddressBlock', 'addressblock'))
        self.addressblock.processForm()

        # Set up plone properties
        self.portal.manage_changeProperties(
            {'email_from_name': 'Plone Admin',
             'email_from_address': 'plone@admin.ch'})

        transaction.commit()

        # Browser setup
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

        self.form = "%s/feedback_view" % self.addressblock.absolute_url()

        # Mock mailhost
        self.mailhost = self.stub()
        self.mock_tool(self.mailhost, 'MailHost')
        self.mails = []
        self.expect(self.mailhost.send(ARGS, KWARGS)).call(
            lambda *args, **kwargs: self.mails.append((args, kwargs)))

        self.replay()

    def _auth(self):
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
            TEST_USER_NAME, TEST_USER_PASSWORD, ))

    def test_cancel_form(self):
        self._auth()
        self.browser.open(self.form)
        self.browser.getControl('Cancel').click()
        self.assertEqual(self.browser.url,
                         self.contentpage.absolute_url())

    def test_required_fields(self):
        self._auth()
        self.browser.open(self.form)
        self.browser.getControl("Send Mail").click()
        self.assertIn('kssattr-fieldname-form.widgets.sender error',
                      self.browser.contents)
        self.assertIn('kssattr-fieldname-form.widgets.email error',
                      self.browser.contents)
        self.assertIn('kssattr-fieldname-form.widgets.subject error',
                      self.browser.contents)
        self.assertIn('kssattr-fieldname-form.widgets.message error',
                      self.browser.contents)

    def test_send_form(self):
        self._auth()
        self.browser.open(self.form)
        self.browser.getControl(
            name="form.widgets.sender").value = FORM_DATA['sender']
        self.browser.getControl(
            name="form.widgets.email").value = FORM_DATA['email']
        self.browser.getControl(
            name="form.widgets.subject").value = FORM_DATA['subject']
        self.browser.getControl(
            name="form.widgets.message").value = FORM_DATA['message']

        self.browser.getControl('Send Mail').click()

        self.assertEqual(self.browser.url,
                         self.contentpage.absolute_url())

        self.assertIn('The email was sent.', self.browser.contents)
        self.assertEquals(len(self.mails), 1)

        args, kwargs = self.mails.pop()
        self.assertIn('=?utf-8?q?Don=27t_p=C3=A4nic?=', args[0].__str__())
        self.assertIn(FORM_DATA['message'], args[0].__str__())
        self.assertIn(
            'Reply-To: =?utf-8?q?Zaph=C3=B6d_Beeblebrox?='
            ' <z.beeblebrox@endofworld.com>',
            args[0].__str__())
        self.assertIn('From: =?utf-8?q?Plone_Admin?= <plone@admin.ch>',
                      args[0].__str__())

    def test_encode_replyto_always(self):
        """Test that tests if Reply-To header is always encoded."""
        self._auth()
        self.browser.open(self.form)
        self.browser.getControl(
            name="form.widgets.sender").value = 'Hans: Peter'
        self.browser.getControl(
            name="form.widgets.email").value = FORM_DATA['email']
        self.browser.getControl(
            name="form.widgets.subject").value = FORM_DATA['subject']
        self.browser.getControl(
            name="form.widgets.message").value = FORM_DATA['message']

        self.browser.getControl('Send Mail').click()

        self.assertEqual(self.browser.url,
                         self.contentpage.absolute_url())

        args, kwargs = self.mails.pop()
        self.assertIn(
            'Reply-To: =?utf-8?q?Hans=3A_Peter?='
            ' <z.beeblebrox@endofworld.com>',
            args[0].__str__())

    def test_comma_in_sender_name_will_be_replaced(self):
        self._auth()
        self.browser.open(self.form)
        self.browser.getControl(
            name="form.widgets.sender").value = 'Zaph\xc3\xb6d,Beeblebrox'
        self.browser.getControl(
            name="form.widgets.email").value = FORM_DATA['email']
        self.browser.getControl(
            name="form.widgets.subject").value = FORM_DATA['subject']
        self.browser.getControl(
            name="form.widgets.message").value = FORM_DATA['message']

        self.browser.getControl('Send Mail').click()

        args, kwargs = self.mails.pop()
        self.assertIn(
            'Reply-To: =?utf-8?q?Zaph=C3=B6d_Beeblebrox?='
            ' <z.beeblebrox@endofworld.com>',
            args[0].__str__())

    def tearDown(self):
        super(TestFeedbackForm, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
        transaction.commit()


class TestFeedbackFormBrowser(TestCase):

    layer = FTW_CONTENTPAGE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        login(self.portal, TEST_USER_NAME)

        self.cpage = create(Builder('content page'))
        self.ablock = create(Builder('address block')
                             .within(self.cpage))

    @browsing
    def test_captcha_is_hidden_if_not_configured(self, browser):
        browser.logout().visit(self.ablock, view="feedback_view")

        # ReCaptcha is in the label which is only
        # rendered if the field is visible
        self.assertFalse(browser.css('#formfield-form-widgets-captcha label'),
                         'The captcha should be hidden.')

    @browsing
    def test_captcha_is_used_if_configured(self, browser):
        registry = getUtility(IRegistry)
        registry['plone.formwidget.recaptcha.interfaces.'
                 'IReCaptchaSettings.private_key'] = u'PRIVATE_KEY'
        registry['plone.formwidget.recaptcha.interfaces.'
                 'IReCaptchaSettings.public_key'] = u'PUBLIC_KEY'
        transaction.commit()

        browser.logout().visit(self.ablock, view="feedback_view")

        self.assertTrue(browser.css('#formfield-form-widgets-captcha label'),
                        'The captcha should be visible.')

    @browsing
    def test_captcha_no_component_lookup_error(self, browser):
        """
        A `ComponentLookupError` was thrown if you first opened the feedback
        form in your browser as an unauthorized user and then opened the
        same feedback form as an authorized user (where the captcha field
        should not be displayed).
        This test makes sure that this does not happen any more. Please see
        `ftw.contentpage.browser.feedback.FeedbackForm#updateWidgets`.
        """
        registry = getUtility(IRegistry)
        registry['plone.formwidget.recaptcha.interfaces.'
                 'IReCaptchaSettings.private_key'] = u'PRIVATE_KEY'
        registry['plone.formwidget.recaptcha.interfaces.'
                 'IReCaptchaSettings.public_key'] = u'PUBLIC_KEY'
        transaction.commit()

        browser.logout().visit(self.ablock, view="feedback_view")
        browser.login().visit(self.ablock, view="feedback_view")

        # Our test passes if the page is loading and contains the feedback
        # form.
        self.assertEqual(len(browser.css('#form')), 1)
