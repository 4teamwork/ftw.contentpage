from ftw.contentpage.testing import FTW_CONTENTPAGE_FUNCTIONAL_TESTING
from ftw.testing import MockTestCase
from mocker import ARGS, KWARGS
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD
import transaction


FORM_DATA = {'sender': 'Zaphod Beeblebrox',
             'email': 'z.beeblebrox@endofworld.com',
             'subject': 'Don\'t panic',
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

        self.assertIn(FORM_DATA['subject'], args[0].__str__())
        self.assertIn(FORM_DATA['message'], args[0].__str__())
        self.assertIn(
            'reply-to: Zaphod Beeblebrox <z.beeblebrox@endofworld.com>',
            args[0].__str__())
        self.assertIn('From: Plone Admin <plone@admin.ch>', args[0].__str__())

    def tearDown(self):
        super(TestFeedbackForm, self).tearDown()
        portal = self.layer['portal']
        portal.manage_delObjects(['contentpage'])
        transaction.commit()
