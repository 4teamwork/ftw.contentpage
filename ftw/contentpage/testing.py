from ftw.builder.session import BuilderSession
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import FunctionalSplinterTesting
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from plone.testing import z2
from zope.configuration import xmlconfig
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent
import ftw.contentpage.tests.builders


class ZCMLLayer(ComponentRegistryLayer):
    """Test layer loading the complete package ZCML.
    """

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.contentpage.tests
        self.load_zcml_file('tests.zcml', ftw.contentpage.tests)

        import ftw.contentpage.browser
        self.load_zcml_file('configure.zcml', ftw.contentpage.browser)


ZCML_LAYER = ZCMLLayer()


def functional_session_factory():
    sess = BuilderSession()
    sess.auto_commit = True
    return sess


class FtwContentPageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.contentpage
        import simplelayout.base
        import ftw.geo
        import collective.geo.settings
        import collective.geo.openlayers
        import collective.geo.geographer
        import collective.geo.contentlocations
        import collective.geo.kml
        import plone.formwidget.contenttree

        xmlconfig.file('configure.zcml', ftw.contentpage,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', simplelayout.base,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', ftw.geo,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.settings,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.openlayers,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.geographer,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.contentlocations,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.geo.kml,
                       context=configurationContext)

        xmlconfig.file('configure.zcml', plone.formwidget.contenttree,
                       context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2
        # products, using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.contentpage')
        z2.installProduct(app, 'simplelayout.base')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.contentpage:default')
        applyProfile(portal, 'simplelayout.base:default')
        applyProfile(portal, 'plone.formwidget.recaptcha:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


class FunctionalBrowserlayerTesting(FunctionalSplinterTesting):
    """Support browserlayer"""

    def setUpEnvironment(self, portal):
        super(FunctionalBrowserlayerTesting, self).setUpEnvironment(portal)

        notify(BeforeTraverseEvent(portal, portal.REQUEST))


class IntegrationBrowserlayerTesting(IntegrationTesting):
    """Support browserlayer"""

    def setUpEnvironment(self, portal):
        super(IntegrationBrowserlayerTesting, self).setUpEnvironment(portal)

        notify(BeforeTraverseEvent(portal, portal.REQUEST))


FTW_CONTENTPAGE_FIXTURE = FtwContentPageLayer()
FTW_CONTENTPAGE_INTEGRATION_TESTING = IntegrationBrowserlayerTesting(
    bases=(FTW_CONTENTPAGE_FIXTURE, ), name="FtwContentPage:Integration")
FTW_CONTENTPAGE_FUNCTIONAL_TESTING = FunctionalBrowserlayerTesting(
    bases=(FTW_CONTENTPAGE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwContentPage:Functional")
