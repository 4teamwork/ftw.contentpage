from ftw.contentpage.content.textblock import TextBlock

faq_schema = paragraph_schema.copy()

if faq_schema.has_key('title'):
    faq_schema['title'].widget.label = u'Frage'
if faq_schema.has_key('text'):
    faq_schema['text'].widget.label = u'Antwort'
if faq_schema.has_key('showTitle'):
    faq_schema['showTitle'].default = True
    faq_schema['showTitle'].widget.visible = -1


class FAQBlock(TextBlock):
