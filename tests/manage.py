import os, sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join('..', BASE_DIR))

CUSTOM_INSTALLED_APPS = (
    'django_google_dork',
)

ALWAYS_INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
)

ALWAYS_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


settings.configure(
    SECRET_KEY="django_tests_secret_key",
    DEBUG=True,
    TEMPLATE_DEBUG=True,
    ALLOWED_HOSTS=[],
    INSTALLED_APPS=ALWAYS_INSTALLED_APPS + CUSTOM_INSTALLED_APPS,
    MIDDLEWARE_CLASSES=ALWAYS_MIDDLEWARE_CLASSES,
    ROOT_URLCONF='tests.urls',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
    LANGUAGE_CODE='en-us',
    TIME_ZONE='UTC',
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
    STATIC_URL='/static/',
    # Use a fast hasher to speed up tests.
    PASSWORD_HASHERS=(
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ),
)

django.setup()
execute_from_command_line(sys.argv)

exit(0)

args = [sys.argv[0], 'test']
path = os.path.dirname('./')
offset = 1

# Allow accessing test options from the command line.
try:
    sys.argv[1]
except IndexError:
    pass
else:
    option = sys.argv[1].startswith('-')
    if not option:
        path = os.path.join(path, sys.argv[1])
        offset = 2

# The second argument points to the current directory.
args.append(path)
# ``verbosity`` can be overwritten from command line.
args.append('--verbosity=2')
args.extend(sys.argv[offset:])

execute_from_command_line(args)
