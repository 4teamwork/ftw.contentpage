from Products.CMFCore.permissions import ManagePortal


DEFAULT_TO_HIDE = [
    'subject', 'relatedItems', 'location', 'language',  # Categorization
    'effectiveDate', 'expirationDate',  # Dates
    'creators', 'contributors', 'rights',  # Contributors
    'allowDiscussion', 'excludeFromNav',  # Settings
    'nextPreviousEnabled',
    ]


def finalize(schema, show=None, hide=None):
    to_hide = DEFAULT_TO_HIDE[:]
    if hide:
        to_hide += hide

    if show:
        for name in show:
            if name in to_hide:
                to_hide.remove(name)

    for name in to_hide:
        if name in schema:
            field = schema[name]
            schema.changeSchemataForField(name, 'default')
            field.widget.visible = {'view': 'invisible', 'edit': 'invisible'}
            field.write_permission = ManagePortal

    # Hide from navigation by default
    schema['excludeFromNav'].default = True
