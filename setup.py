#!/usr/bin/env python

from setuptools import setup

setup(
    name='django-google-dork',
    version='0.1',
    description='A django app to manage Google dorks, run them and cache results.',
    author='Christian Gagneraud',
    author_email='chgans@gna.org',
    url='http://github.com/chgans/django-google-dork',
    packages=[
        'django_google_dork',
        ],
    package_dir={'': '.'},
    install_requires=[
        "django",
        "django-model-utils",
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP',
        ]
    )
