#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='nosmsd',
    version=__import__('nosmsd').__version__,
    license='GNU Lesser General Public License (LGPL), Version 3',

    install_requires=['peewee>=0.7.4'],
    provides=['nosmsd'],

    description='Python wrapper around Gammu-smsd Database.',
    long_description=open('README').read(),
    author='yɛlɛman s.à.r.l',
    author_email='reg@yeleman.com',

    url='http://github.com/yeleman/nosmsd',

    keywords="sms gammu smsd",
    packages=['nosmsd'],

    scripts=['nosmsd/nosmsd_incoming.py',
             'nosmsd/nosmsd_incoming_venv.py',
             'nosmsd/nosmsd_inject.py',
             'nosmsd/nosmsd_sendout.py'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
)
