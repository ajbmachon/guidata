# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (copied from Spyder source code [spyderlib.qt])

"""Transitional package (PyQt4 --> PySide)"""

import os

_modname = os.environ.setdefault('PYTHON_QT_LIBRARY', 'PyQt4')

if _modname == 'PyQt4':
    import sip
    try:
        sip.setapi('QString', 1)
        sip.setapi('QVariant', 1)
    except AttributeError:
        # PyQt < v4.6: in future version, we should warn the user 
        # that PyQt is outdated and won't be supported by Spyder >v2.1
        pass
