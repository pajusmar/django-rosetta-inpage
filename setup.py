#!/usr/bin/env python
from distutils.core import setup
import sparky_client

setup(
    name='sparky_client',
    version=sparky_client.__version__,
    description='Translate Django messages inline with a cache and database backend',
    author='VikingCo NV',
    author_email='maarten.huijsmans@mobilevikings.com',
    url='http://github.com/citylive/sparky-client/',
    packages=['sparky_client'],
    license='BSD',
    include_package_data = True,
    package_data = {'spark_client': ['templates/sparky_client/*'],},
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