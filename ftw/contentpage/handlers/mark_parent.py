from ftw.contentpage.interfaces import IOrgUnitMarker
from zope.interface import noLongerProvides
from zope.interface import alsoProvides
from Acquisition import aq_parent
from Acquisition import aq_inner
from borg.localrole.interfaces import IFactoryTempFolder


class MarkBase(object):

    context = None
    parent = None
    event = None

    def __init__(self, obj, event):
        self.context = obj
        self.parent = aq_parent(aq_inner(self.context))
        self.event = event

    def mark(self):
        if not IOrgUnitMarker.providedBy(self.parent):
            alsoProvides(self.parent, IOrgUnitMarker)
            self.parent.reindexObject(idxs=['object_provides'])

    def unmark(self):
        noLongerProvides(self.parent, IOrgUnitMarker)
        self.parent.reindexObject(idxs=['object_provides'])

    def has_one_addressblock(self):
        result = self.parent.getFolderContents(
            contentFilter={'portal_type': ['AddressBlock']})
        return bool(len(result) == 1)

    def is_triggered_by_addressblock(self):
        # Only Fire events on AddressBlocks
        # Example: OFS.interfaces.IObjectWillBeRemovedEvent will be also
        # fired on Addressblock if the contentpage will be deleted
        return bool(self.event.object.portal_type == 'AddressBlock')


class MarkParent(MarkBase):

    def __init__(self, obj, event):
        super(MarkParent, self).__init__(obj, event)
        self.mark()


class UnMarkParent(MarkBase):
    def __init__(self, obj, event):
        super(UnMarkParent, self).__init__(obj, event)
        if not self.is_triggered_by_addressblock():
            return

        if not self.has_one_addressblock():
            self.unmark()


class AddMoveCopy(MarkBase):
    def __init__(self, obj, event):
        super(AddMoveCopy, self).__init__(obj, event)

        # Do nothing if we are in the factory
        if IFactoryTempFolder.providedBy(self.parent):
            return None

        # Move
        if self.event.oldParent and self.event.newParent:
            self.mark()

            self.parent = self.event.oldParent
            self.unmark()

        # Copy / Add
        if self.event.newParent and not self.event.oldParent:
            self.mark()
