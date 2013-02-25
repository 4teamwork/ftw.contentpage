from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from simplelayout.base.interfaces import IBlockConfig
from zope.component import getUtility
from zope.component import queryMultiAdapter
from simplelayout.base.interfaces import IScaleImage


class TextBlockView(BrowserView):

    def __init__(self, context, request):
        super(TextBlockView, self).__init__(context, request)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        self.blockconf = IBlockConfig(self.context)
        self.image_layout = self.blockconf.image_layout

    def get_css_klass(self):
        layout = self.image_layout
        return 'sl-img-' + layout

    def has_image(self):
        return bool(self.context.getImage())

    def get_image_tag(self):
        alt = unicode(self.context.getImageAltText(),
                      self.context.getCharset())
        title = unicode(self.context.getImageCaption(),
                        self.context.getCharset())

        if not title:
            title = alt

        image_util = getUtility(
            IScaleImage,
            name='simplelayout.image.scaler')
        img_attrs = image_util.get_image_attributes(self.context)
        scales = queryMultiAdapter((self.context, self.request), name="images")

        if img_attrs['width'] == 0 and img_attrs['height'] == 0:
            # either there is no image or we use a layout such as
            # "no-image" which does not show the image - we do not
            # need to create a scale in this case nor to return a
            # <img> HTML tag.
            return ''

        return scales.scale(
            'image',
            width=img_attrs['width'],
            height=img_attrs['height']).tag(title=title, alt=alt)

    def image_wrapper_style(self):
        """ sets width of the div wrapping the image, so the
        caption will shown under the image
        """

        image_util = getUtility(
            IScaleImage,
            name='simplelayout.image.scaler')
        img_attrs = image_util.get_image_attributes(self.context)
        return "width: %spx" % img_attrs['width']

    def get_block_height(self):
        height = self.blockconf.block_height
        return height and 'height: %spx' % height or ''
