from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.upgrade import UpgradeStep
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContent
from plone.uuid.interfaces import IMutableUUID
from plone.uuid.interfaces import IUUID


class ToSimplelayout(UpgradeStep):

    def __call__(self):
        oldpage = self.portal.get('die-inhaltsseite')
        newpage = self.replace_object(oldpage, 'ftw.simplelayout.ContentPage')
        newpage.setTitle(oldpage.Title())
        newpage.setDescription(oldpage.Description() + ';; migrated!!')
        newpage.reindexObject()

        oldblock = newpage.get('ein-textblock')
        newblock = self.replace_object(oldblock, 'ftw.simplelayout.TextBlock')
        newblock.setTitle(oldblock.Title())
        newblock.text = RichTextValue(
            raw=(oldblock.getText() + ';; migrated!!').decode('utf-8'),
            mimeType='text/html',
            outputMimeType='text/x-html-safe')
        newblock.reindexObject()

        import pdb; pdb.set_trace()

    def replace_object(self, oldobj, new_portal_type):
        newobj = createContent(new_portal_type)
        newobj.id = oldobj.id
        IMutableUUID(newobj).set(IUUID(oldobj))

        for name in ('__ac_local_roles__',
                     '__annotations__',
                     '_tree',
                     '_mt_index',
                     '_count'):
            if hasattr(aq_base(oldobj), name):
                setattr(aq_base(newobj), name, getattr(aq_base(oldobj), name))

        parent = aq_parent(aq_inner(oldobj))
        parent._delOb(oldobj.id)
        parent._setOb(oldobj.id, newobj)
        return parent._getOb(oldobj.id)
