# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
GUI-based test launcher
"""

import sys, os, os.path as osp, subprocess
from PyQt4.QtGui import (QWidget, QVBoxLayout, QSplitter, QFont, QListWidget,
                         QPushButton, QLabel, QGroupBox, QHBoxLayout, QShortcut,
                         QKeySequence)
from PyQt4.QtCore import SIGNAL, Qt, QSize
from PyQt4.Qsci import QsciScintilla, QsciLexerPython

from guidata.config import _
from guidata.configtools import get_icon, get_family, MONOSPACE
from guidata.qthelpers import get_std_icon


def get_tests(test_package):
    tests = []
    test_path = osp.dirname(osp.realpath(test_package.__file__))
    for fname in sorted(os.listdir(test_path)):
        module_name, ext = osp.splitext(fname)
        if ext not in ('.py', '.pyw'):
            continue
        if not module_name.startswith('_'):
            _temp = __import__(test_package.__name__, fromlist=[module_name])
            test_module = getattr(_temp, module_name)
            test = TestModule(test_module)
            if test.is_visible():
                tests.append(test)
    return tests


class TestModule(object):
    def __init__(self, test_module):
        self.module = test_module
        self.filename = osp.splitext(osp.abspath(test_module.__file__))[0]+'.py'
        if not osp.isfile(self.filename):
            self.filename += 'w'
        
    def is_visible(self):
        return hasattr(self.module, 'SHOW') and self.module.SHOW
    
    def get_description(self):
        doc = self.module.__doc__
        if doc is None or not doc.strip():
            return _("No description available")
        else:
            lines = doc.strip().splitlines()
            format = '<span style=\'color: #2222FF\'><b>%s</b></span>'
            lines[0] = format % lines[0]
            return '<br>'.join(lines)
    
    def get_code(self):
        return unicode(file(self.filename, 'rb').read(), 'utf-8')
    
    def run(self, args=''):
        command = [sys.executable, '"'+self.filename+'"']
        if args:
            command.append(args)
        subprocess.Popen(" ".join(command), shell=True)


class TestPropertiesWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        font = QFont(get_family(MONOSPACE), 9, QFont.Normal)
        
        info_icon = QLabel()
        icon = get_std_icon('MessageBoxInformation').pixmap(24, 24)
        info_icon.setPixmap(icon)
        info_icon.setFixedWidth(32)
        info_icon.setAlignment(Qt.AlignTop)
        self.desc_label = QLabel()
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignTop)
        self.desc_label.setFont(font)
        group_desc = QGroupBox(_("Description"), self)
        layout = QHBoxLayout()
        layout.addWidget(info_icon)
        layout.addWidget(self.desc_label)
        group_desc.setLayout(layout)
        
        self.editor = QsciScintilla(self)
        lexer = QsciLexerPython()
        lexer.setFont(font)
        self.editor.setLexer(lexer)
        self.editor.setReadOnly(True)
        self.editor.setMarginLineNumbers(1, True)
        self.editor.setMarginWidth(1, 25)
        group_code = QGroupBox(_("Source code"), self)
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        group_code.setLayout(layout)
        
        self.run_button = QPushButton(get_icon("apply.png"),
                                      _("Run this script"), self)
        self.run_all_button = QPushButton(get_icon("busy.png"),
                                          _("Run all tests"), self)
        self.quit_button = QPushButton(get_icon("exit.png"), _("Quit"), self)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.run_button)
        hlayout.addStretch()
        hlayout.addWidget(self.run_all_button)
        hlayout.addStretch()
        hlayout.addWidget(self.quit_button)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(group_desc)
        vlayout.addWidget(group_code)
        vlayout.addLayout(hlayout)
        self.setLayout(vlayout)
        
    def set_item(self, test):
        self.desc_label.setText(test.get_description())
        self.editor.setText(test.get_code())


class TestLauncherWindow(QSplitter):
    def __init__(self, package, parent=None):
        QSplitter.__init__(self, parent)
        self.setWindowTitle(_("Tests - %s module") % package.__name__)
        self.setWindowIcon(get_icon("%s.png" % package.__name__, "guidata.png"))
        
        test_package_name = '%s.tests' % package.__name__
        _temp = __import__(test_package_name)
        test_package = sys.modules[test_package_name]
        
        tests = get_tests(test_package)
        listwidget = QListWidget(self)
        listwidget.addItems([osp.basename(test.filename) for test in tests])
        
        self.properties = TestPropertiesWidget(self)
        
        self.addWidget(listwidget)
        self.addWidget(self.properties)
        
        self.connect(self.properties.run_button, SIGNAL("clicked()"),
                     lambda: tests[listwidget.currentRow()].run())
        self.connect(self.properties.run_all_button, SIGNAL("clicked()"),
                     lambda: [test.run() for test in tests])
        self.connect(self.properties.quit_button, SIGNAL("clicked()"),
                     self.close)
        self.connect(listwidget, SIGNAL('currentRowChanged(int)'),
                     lambda row: self.properties.set_item(tests[row]))
        self.connect(listwidget, SIGNAL('itemActivated(QListWidgetItem*)'),
                     lambda: tests[listwidget.currentRow()].run())
        listwidget.setCurrentRow(0)
        
        QShortcut(QKeySequence("Escape"), self, self.close)
            
        self.setSizes([150, 1])
        self.setStretchFactor(1, 1)
        self.resize(QSize(800, 600))
    

def run_testlauncher(package):
    """Run test launcher"""
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    win = TestLauncherWindow(package)
    win.show()
    app.exec_()
    