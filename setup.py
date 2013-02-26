#!/usr/bin/env python
from distutils.core import setup
import rosetta_inpage

setup(
    name='rosetta_inpage',
    version=rosetta_inpage.__version__,
    description='Translate i18n messages with Django Rosetta',
    author='VikingCo NV',
    author_email='maarten.huijsmans@mobilevikings.com',
    url='http://github.com/citylive/django-rosetta-inpage/',
    packages=['rosetta_inpage'],
    license='BSD',
    include_package_data = True,
    package_data = {'rosetta_inpage': ['templates/rosetta_inpage/*'],},
    zip_safe = False,
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Software Development :: Internationalization',
        ],
    requires=[
        'django',
	'django-rosetta',
    ],
)


