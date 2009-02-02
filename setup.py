from setuptools import setup, find_packages

setup(
    name = 'django-openid',
    version = '0.1.3',
    description = 'django-openid provides tools for dealing with OpenID '
                  'in your Django applications.',
    long_description = 'django-openid provides tools for dealing with OpenID '
                  'in your Django applications, with smart default settings '
                  'designed to get you up and running as quickly as possible '
                  'combined with simple hooks for customising any aspect of the OpenID flow.',
    keywords = 'django openid',
    author = 'Simon Willison',
    author_email = 'simon@simonwillison.net',
    maintainer = 'Alexander Artemenko',
    maintainer_email = 'svetlyak.40wt@gmail.com',
    url = 'http://code.google.com/p/django-openid/',
    dependency_links = ['http://aartemenko.com/media/packages.html'],
    install_requires = ['python-openid'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(exclude=['django_openidconsumer*', 'example_consumer*', 'django_openid.tests*']),
    include_package_data = True,
)

