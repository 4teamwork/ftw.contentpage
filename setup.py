import os
from setuptools import setup, find_packages


version = '1.0.dev0'
mainainter = 'Mathias Leimgruber'

tests_require = ['ftw.testing',
                 'plone.app.testing',
                 'plone.mocktestcase', ]

setup(name='ftw.contentpage',
      version=version,
      description="Contentpage based on Simplelayout for for web/intranet",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='ftw contentpage',
      author='4teamwork GmbH',
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
          'setuptools',
          'simplelayout.base',
          'simplelayout.portlet.dropzone',
          'archetypes.schemaextender',
          'ftw.geo',
          'ftw.table',
      ],

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
