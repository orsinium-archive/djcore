#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name     = 'djcore',
    version  = '0.5.0',
    
    author       = 'orsinium',
    author_email = 'master_fess@mail.ru',
    
    description  = 'Core 4 django.',
    long_description = open('README.md').read(), 
    keywords     = 'django core utils',
    
    packages = ['djcore'],
    requires = ['python (>= 3.4)'],
    
    url          = 'https://github.com/orsinium/djcore',
    download_url = 'https://github.com/orsinium/djcore/tarball/master',
    
    license      = 'GNU Lesser General Public License v3.0',
    classifiers  = [
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
    ],
)
