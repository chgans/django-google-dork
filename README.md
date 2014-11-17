django-google-dork 
==================

[![License](http://img.shields.io/pypi/l/django-google-dork.svg)](https://github.com/chgans/django-google-dork/blob/master/LICENSE.md)
[![Documentation](https://readthedocs.org/projects/pip/badge/)](https://django-google-dork.readthedocs.org)
[![pypi version](http://img.shields.io/pypi/v/django-google-dork.svg)](https://pypi.python.org/pypi/django-google-dork) 
[![pypi download month](http://img.shields.io/pypi/dm/django-google-dork.svg)](https://pypi.python.org/pypi/django-google-dork) 
[![Build Status](https://travis-ci.org/chgans/django-google-dork.svg?branch=master)](https://travis-ci.org/chgans/django-google-dork) 
[![Coverage Status](http://img.shields.io/coveralls/chgans/django-google-dork.svg)](https://coveralls.io/r/chgans/django-google-dork?branch=master)

A django app to manage Google dorks, run them and cache results.

Status
=======

**This is highly experimental, unfinished, work in progress.**

If you're looking for something you can use, they try again later...

The reason I'm publishing packages and documentation publically is
because this is part of my continuous integration system.

As soon as the code is usable and has sufficient features, I will
publish it as version 1.0.

Anything with a version lower than 1.0 is not guarented to work as the
documentation said, althrough I will publish only version of the
code that pass the build and the test steps.


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
* Add template for dork progress indicators (Jobtastic w/ jquery-celery)

Documentation
=============
[Read the docs &rarr;](https://django-google-dork.readthedocs.org)
