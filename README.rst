Introduction
============

``ftw.contentpage`` provides some content types optimized for organisations,
communities, associations, and more.

It uses simplelayout to manage and display the content.

Installing
==========

- Add ``ftw.contentpage`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.contentpage

- Install the generic import profile.


Usage
=====

**Types:**

- ContentPage: Folderish type for the site structure. Contains the blocks
- AddressBlock: AddressBlock contains address informations and it ``uses ftw.geo`` to render a map
- ListingBlock: A folderish block, which lists files and images by default. Two block views are provided: Tabular listing and a gallery view.

**Special views:**

There's a two-column and two-level overview called authorities_view, which displays a list of ContentPages with an AddressBlock.
If an AddressBlock is added to a ContentPage, it adds a marker interface on the ContentPage, so it's easy to recognize ContentPage's containing an AddressBlock.

**ContentListing viewlet:**

The content listing viewlet is registered for all ContentPages.
It shows categorized subcontent, within the ContentPage
The categorization is done by a schemaextended field, so it's also possible to categorize your own or any other content.

Code example:

::

  <class class="dotted.name.to.my.class">
    <implements interface="ftw.contentpage.interfaces.ICategorizable" />
  </class>


``ftw.contentpage`` is using the additional slot provided by simplelayout
(implements the IAdditionalListingEnabled interface of simplelayout)

So the layout has the following structure:

1. Simplelayout main slot for blocks
2. The content listing viewlet
3. The additional slot for blocks

This way it's possible to display content below the content listing viewlet (by drag'n'drop)



Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.contentpage
- Issue tracker: https://github.com/4teamwork/ftw.contentpage/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.contentpage
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.contentpage


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contentpage`` is licensed under GNU General Public License, version 2.
