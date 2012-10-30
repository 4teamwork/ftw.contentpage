from AccessControl import ClassSecurityInfo
from ftw.contentpage.interfaces import IAddressBlock
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.types.common import config
from simplelayout_schemas import finalize_simplelayout_schema
from zope.interface import implements


from Products.ATContentTypes.config import HAS_LINGUA_PLONE
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone import public as atapi
else:
    from Products.Archetypes import atapi

schema = atapi.Schema((
     atapi.BooleanField(
                'showTitle',
                schemata='default',
                default=0,
                widget=atapi.BooleanWidget(
                    description="Show title",
                    description_msgid="simplelayout_help_showtitle",
                    label="Show Title",
                    label_msgid="simplelayout_label_showtitle",
                    i18n_domain="simplelayout",
                    )),
))


addressblock_schema = ATContentTypeSchema.copy() + schema.copy()

addressblock_schema['excludeFromNav'].default = True
addressblock_schema['excludeFromNav'].visible = -1
addressblock_schema['title'].required = False
finalize_simplelayout_schema(addressblock_schema)
addressblock_schema['description'].widget.visible = {'edit': 0, 'view': 0}


class AddressBlock(ATDocumentBase):
    """
    """
    security = ClassSecurityInfo()
    implements(IAddressBlock, ISimpleLayoutBlock)
    schema = addressblock_schema


atapi.registerType(AddressBlock, config.PROJECTNAME)
