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
- ListingBlock: A folderish block, which lists files and images by default. Two block views are provided: Tabular listing and a gallery view. The columns of the file listing are configurable per block. The default set of columns is configured through the the registry (plone.app.registry). The default sort order of the Listingblock file listing can be configured per block.
- EventPage / EventFolder: A simple and minimal event implementation based on a ContentPage.
- News / NewsFolder: A simple news implementation based on a ContentPage.

**Special views:**

There's a two-column and two-level overview called authorities_view, which displays a list of ContentPages with an AddressBlock.
If an AddressBlock is added to a ContentPage, it adds a marker interface on the ContentPage, so it's easy to recognize ContentPage's containing an AddressBlock.

The EventFolder has a simple events listing, which shows the next 10 upcoming events (batching included).

The NewsFolder has a simple news listing, which shows the 10 most recent news entries (batching included).

**ContentListing viewlet:**

The content listing viewlet is registered for all ContentPages.
It shows categorized subcontent, within the ContentPage
The categorization is done by a schemaextended field, so it's also possible to categorize your own or any other content.

** Teaser Image **
All content pages, event pages and news are able to display a teaser image, which is stored
on the content itself. It behaves like a regular block and shows also the description.
The teaser image related fields have their own write permission, one per content type.
Take a look at the `rolemap.xml` for details.

** Portlet **
It's possible to enable an archive portlet for News and EventPages.
It only works if the current view is the news or event listing view.
The portlet is not created by default.

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


**ftw.lawgiver support**

``ftw.contentpage`` supports ``ftw.lawgiver``

Check: https://github.com/4teamwork/ftw.lawgiver


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.1`, `4.2` or `4.3`.


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

.. image:: https://cruel-carlota.pagodabox.com/d3e4ca26391a0beac20e5c8ff77e5559
   :alt: githalytics.com
   :target: http://githalytics.com/4teamwork/ftw.contentpage
