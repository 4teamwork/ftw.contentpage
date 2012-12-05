from ftw.contentpage.content.textblock import TextBlock
from ftw.upgrade import ProgressLogger
from ftw.upgrade import UpgradeStep
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from ftw.contentpage.interfaces import ITextBlock
from ftw.contentpage.interfaces import IContentPage
from Acquisition import aq_parent


class MigrateParagraphs(UpgradeStep):
    """Migrates simplelayout.types.common Paragraphs to
    ftw.contentpage TextBlocks.
    """

    def __call__(self):

        self.install_upgrade_profile()
        self.migrate_paragraphs()

    def install_upgrade_profile(self):
        self.setup_install_profile(
            'profile-ftw.contentpage.upgrades:1001')

    def migrate_paragraphs(self):

        try:
            from simplelayout.types.common.interfaces import IParagraph
        except ImportError:
            raise

        result = self.catalog_unrestricted_search(
            {'portal_type': 'Paragraph'}, full_objects=True)
        result = list(result)
        with ProgressLogger('Migrate Paragraphs', result) as step:
            for obj in result:
                if not IContentPage.providedBy(aq_parent(obj)):
                    continue
                self.migrate_class(obj, TextBlock)
                obj.portal_type = 'TextBlock'

                noLongerProvides(obj, IParagraph)
                alsoProvides(obj, ITextBlock)

                obj.reindexObject()
                step()
