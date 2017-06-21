import os
from setuptools import setup, find_packages


version = '1.16.1'
mainainter = 'Mathias Leimgruber'

tests_require = ['ftw.testing [splinter] <1.12.0',
                 'ftw.testbrowser',
                 'ftw.builder',
                 'plone.app.testing',
                 'plone.mocktestcase',
                 'plone.formwidget.contenttree',
                 'ftw.calendar >= 3.0.0',
                 'pyquery',
                 ]

setup(name='ftw.contentpage',
      version=version,
      description="Contentpage based on Simplelayout for for web/intranet",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw contentpage',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.contentpage',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      install_requires=[
          'Plone',
          'archetypes.schemaextender',
          'collective.quickupload',
          'collective.geo.openlayers >= 3.0, < 4.0',
          'collective.geo.mapwidget >= 2.1, < 3.0',
          'ftw.calendarwidget',
          'ftw.colorbox',
          'ftw.geo',
          'ftw.profilehook',
          'ftw.table',
          'ftw.upgrade',
          'plone.api >= 1.3.2',
          'plone.formwidget.contenttree',
          'plone.formwidget.recaptcha',
          'setuptools',
          'simplelayout.base>=4.0.2',
          'simplelayout.ui.base >= 3.0.3',
          'simplelayout.portlet.dropzone',
          'plone.dexterity',
          'plone.directives.form',
          ],

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
