from pkg_resources import get_distribution


PROJECTNAME = 'ftw.contentpage'


ADD_PERMISSIONS = {
    'ContentPage': 'ftw.contentpage: Add ContentPage',
    'AddressBlock': 'ftw.contentpage: Add AddressBlock',
    'ListingBlock': 'ftw.contentpage: Add ListingBlock',
    'TextBlock': 'ftw.contentpage: Add TextBlock',
    'News': 'ftw.contentpage: Add News',
    'NewsFolder': 'ftw.contentpage: Add NewsFolder',
    'EventPage': 'ftw.contentpage: Add EventPage',
    'EventFolder': 'ftw.contentpage: Add EventFolder',
    }

INDEXES = (('getContentCategories', 'KeywordIndex'),
          ('getContentType', 'FieldIndex'))


ORIGINAL_SIZE = (900, 900)



if get_distribution('Plone').version >= '4.3':
    HAS_CONTENT_LISTING_BEHAVIOR = True
else:
    HAS_CONTENT_LISTING_BEHAVIOR = False
