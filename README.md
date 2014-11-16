django-google-dork 
==================

[![License](http://img.shields.io/pypi/l/django-google-dork.svg)](https://github.com/chgans/django-google-dork/blob/master/LICENSE.md)
[![pypi version](http://img.shields.io/pypi/v/django-google-dork.svg)](https://pypi.python.org/pypi/django-google-dork) 
[![pypi download month](http://img.shields.io/pypi/dm/django-google-dork.svg)](https://pypi.python.org/pypi/django-google-dork) 
[![Build Status](https://travis-ci.org/chgans/django-google-dork.svg?branch=master)](https://travis-ci.org/chgans/django-google-dork) 
[![Coverage Status](http://img.shields.io/coveralls/chgans/django-google-dork.svg)](https://coveralls.io/r/chgans/django-google-dork?branch=master)

A django app to manage Google dorks, run them and cache results.

Status
======

This is very early code. It builds sucessfully (with Django-1.7.1),
there's a good test suite, it is even usable but it definitely need
proper documentation. Will come soon, stay tuned

TODO
====

By priority order:

* Add downloader concept
* Add admin models
* Add support for async tasks (rabbitmq) and tests
* Test with multiple DB (sqlite, mysql, posgres) to make sure we're UTF-8 compliant
* Add tests with non latin/western encoding (russian, chinese, ...)
* refactor custom fields (Campaign and Dork)
* Make sure PyPi packages are working correctly
* Write comprehensive documentation (installation, concepts and rational, usage, dev & test, API, ...)
* Improve coverage
* Add blacklisting and/or url match/exclude patterns (all regexp)
* Add initial data?

Documentation
=============
[Read the docs &rarr;](https://django-google-dork.readthedocs.org)
