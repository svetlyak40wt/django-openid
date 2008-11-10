from setuptools import setup, find_packages

setup(
    name = 'django-openid',
    version = '0.1.0',
    description = 'django-openid provides tools for dealing with OpenID '
                  'in your Django applications.',
    long_description = 'django-openid provides tools for dealing with OpenID '
                  'in your Django applications, with smart default settings '
                  'designed to get you up and running as quickly as possible '
                  'combined with simple hooks for customising any aspect of the OpenID flow.',
    packages = find_packages(exclude=['django_openidconsumer*', 'example_consumer*', 'django_openid.tests*']),
    include_package_data = True,
)

