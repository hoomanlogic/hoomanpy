from distutils.core import setup

VERSION = '0.1.0'
desc    = """Extended objects and common utilities for Python."""

setup(name='hoomanpy',
        version=VERSION, 
        author='Geoffrey Floyd',
        author_email='geoffrey.floyd@hoomanlogic.com',
        url='http://github.com/hoomanlogic/querylist/',
        download_url='https://pypi.python.org/pypi/querylist/',
        description='Python. Improved.',
        license='http://www.apache.org/licenses/LICENSE-2.0',
        py_modules =['hoomanpy'],
        platforms=['Any'],
        long_description=desc,
        classifiers=['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Apache Software License',
                     'Operating System :: OS Independent',
                     'Topic :: Text Processing',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7'
                    ]
        )