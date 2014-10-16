from setuptools import setup, find_packages

setup(
    name="django-snappy-vumi-bouncer",
    version="0.2.0",
    url='https://github.com/westerncapelabs/django-snappy-vumi-bouncer',
    license='BSD',
    description=(
        "A Django app that bounces messages from Vumi to Snappy and back"),
    long_description=open('README.rst', 'r').read(),
    author='Western Cap Labs',
    author_email='devops@westerncapelabs.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
        'django-tastypie',
        'besnappy',
        'django-celery',
        'go_http',
        'South',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],
)
