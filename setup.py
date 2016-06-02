from setuptools import setup


setup(
    name='flask-statsd-tags',
    version='0.1.2',
    url='https://github.com/flask-statsd/',
    license='BSD',
    author='gfreezy',
    author_email='gfreezy@gmail.com',
    description='Flask extention for sending statsd data',
    long_description=__doc__,
    py_modules=['flask_statsd'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'statsd',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
