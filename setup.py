#!/usr/bin/env python
from distutils.core import setup
import sprak

setup(
    name='django-sprak',
    version=sprak.__version__,
    description='Translate Django messages inline with a cache and database backend',
    author='VikingCo NV',
    author_email='jef.geskens@mobilevikings.com',
    url='http://github.com/citylive/django-sprak/',
    packages=['sprak'],
    license='BSD',
    include_package_data = True,
    package_data = {'sprak': ['templates/sprak/*'],},
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
)