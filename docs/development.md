# Development setup 

# Running tests

# Continuous integration with [Travis](https://travis-ci.org)

# Things to do in order to cut a new release

## Passing Tests

Make sure that all of the tests on travis-ci have run and are passing.

## Bump the version

Editing `django_google_dork/__init__.py` and increment the version
according to the [Semantic Versioning](http://semver.org/) standard.

**TODO: have a simple script to do that?**

## Changelog

Ensure that the `CHANGELOG.md` file includes all relevant changes.

**TODO: Create this file!**

## Documentation is up to date

Ensure that any new features are documented
and give the docs a read-through
to make sure they haven't started lying.

## Publish documentation

Documentation is automatically rebuild by [RTD](https://readthedocs.org).
But we need to make sure that the doc versioning follows the package versioning.

## Build and push the package to PyPi

1. Run `$ python setup.py sdist` to make sure the package is kosher.
  Correct any errors or warnings that appear and commit those changes.
1. Check the package file to ensure that it has the files we want.
1. Push to PyPi! `$ python setup.py sdist upload`

**TODO: script automation?**

## Tag the version

Use git to tag the version according to
the[Semantic Versioning](http://semver.org/) standard.

eg. `$ git tag v0.1.1 && git push --tags`

## Post the Changelog to the Github releases page

Browse to the [releases page](https://github.com/PolicyStat/jobtastic/releases)
and edit our newly-tagged release with a title
and the relevant Changelog sections.

## Consider announcing things

If the new version adds something sufficiently cool,
consider posting to the celery mailing list.
Also consider posting to G+, Twitter, etc.
so that folks who would find Jobtastic useful can actually find it.

## NB
This page was based on a good idea by [Jobtastic](https://github.com/PolicyStat/jobtastic/blob/a855620becd5d744936b57e1136ab38d49ee7404/release_checklist.md)
