#!/usr/bin/env python
"""
Register the package on pypi:
python setup.py register

Upload the package to pypi:
python setup.py sdist upload

List of classifiers:
https://pypi.python.org/pypi?%3Aaction=list_classifiers
"""
from setuptools import setup
import rosetta_inpage

LONG_DESCRIPTION = """\
rosette_inpage is built of django-rosetta.  It allows you to translate django applications directly in a page, it adds
an extra toolbar to each and lists all the strings that can be translated on that page. The changes are saved directly
to the according po files.

This allows non-technical people to easily translate django applications and to have context while translating strings
"""

setup(
    name='rosetta_inpage',
    version=rosetta_inpage.__version__,
    description='Translate i18n messages with Django Rosetta',
    long_description=LONG_DESCRIPTION,
    author='Maarten Huijsmans, VikingCo NV',
    author_email='maarten.huijsmans@mobilevikings.com',
    url='http://github.com/citylive/django-rosetta-inpage/',
    packages=['rosetta_inpage'],
    license='BSD',
    include_package_data=True,
    package_data={'rosetta_inpage': ['templates/rosetta_inpage/*'], },
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Software Development :: Internationalization',
    ],
    install_requires=[
        'Django >= 1.3',
        'django-rosetta == 0.6.8'
    ]
)


