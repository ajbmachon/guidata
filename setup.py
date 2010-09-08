# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
guidata
=======

Set of basic GUIs to edit and display objects of many kinds:
    - integers, floats, strings ;
    - ndarrays (NumPy's n-dimensional arrays) ;
    - etc.

Copyright © 2009-2010 CEA
Pierre Raybaut
Licensed under the terms of the CECILL License
(see guidata/__init__.py for details)
"""

from distutils.core import setup
import os, os.path as osp


def get_package_data(name, extlist):
    """
    Return data files for package *name* with extensions in *extlist*
    (search recursively in package directories)
    """
    assert isinstance(extlist, (list, tuple))
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name)+len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        for fname in filenames:
            if osp.splitext(fname)[1] in extlist:
                flist.append(osp.join(dirpath, fname)[offset:])
    return flist


LIBNAME = 'guidata'
from guidata import __version__ as version

DESCRIPTION = 'guidata is a set of basic GUIs to edit and display objects of many kinds'
LONG_DESCRIPTION = """Set of basic GUIs to edit and display objects of many kinds:
    - integers, floats, strings ;
    - ndarrays (NumPy's n-dimensional arrays) ;
    - etc."""
KEYWORDS = ''
CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Topic :: Scientific/Engineering']

PACKAGES = [LIBNAME+p for p in ['', '.dataset', '.tests']]
PACKAGE_DATA = {LIBNAME: get_package_data(LIBNAME, ('.png', '.mo'))}

if os.name == 'nt':
    SCRIPTS = ['guidata-tests.py']
else:
    SCRIPTS = ['guidata-tests']

setup(name=LIBNAME, version=version,
      description=DESCRIPTION, long_description=LONG_DESCRIPTION,
      packages=PACKAGES, package_data=PACKAGE_DATA,
      scripts=SCRIPTS,
      requires=["PyQt4 (>4.3)",],
      author = "Pierre Raybaut",
      author_email = 'pierre.raybaut@cea.fr',
      url = 'http://www.cea.fr',
      classifiers=CLASSIFIERS + [
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        ],
      )
