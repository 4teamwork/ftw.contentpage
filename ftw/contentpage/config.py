PROJECTNAME = 'ftw.contentpage'


ADD_PERMISSIONS = {
    'ContentPage': 'ftw.contentpage: Add ContentPage',
    'AddressBlock': 'ftw.contentpage: Add AddressBlock',
    'ListingBlock': 'ftw.contentpage: Add ListingBlock',
}

INDEXES = (('getCategories', 'KeywordIndex'),
          ('getContentType', 'FieldIndex'))
