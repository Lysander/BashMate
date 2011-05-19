# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_commanddialog.ui'
#
# Created: Thu May 19 15:59:01 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CommandDialog(object):
    def setupUi(self, CommandDialog):
        CommandDialog.setObjectName(_fromUtf8("CommandDialog"))
        CommandDialog.resize(400, 300)
        self.formLayout = QtGui.QFormLayout(CommandDialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(CommandDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.commandEdit = QtGui.QLineEdit(CommandDialog)
        self.commandEdit.setObjectName(_fromUtf8("commandEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.commandEdit)
        self.label_2 = QtGui.QLabel(CommandDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.infoEdit = QtGui.QTextEdit(CommandDialog)
        self.infoEdit.setObjectName(_fromUtf8("infoEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.infoEdit)
        self.label_3 = QtGui.QLabel(CommandDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.namesView = QtGui.QListView(CommandDialog)
        self.namesView.setObjectName(_fromUtf8("namesView"))
        self.horizontalLayout.addWidget(self.namesView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.nameEdit = QtGui.QLineEdit(CommandDialog)
        self.nameEdit.setEnabled(True)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.verticalLayout.addWidget(self.nameEdit)
        self.addButton = QtGui.QPushButton(CommandDialog)
        self.addButton.setEnabled(False)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(CommandDialog)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(CommandDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(CommandDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CommandDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CommandDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CommandDialog)

    def retranslateUi(self, CommandDialog):
        CommandDialog.setWindowTitle(QtGui.QApplication.translate("CommandDialog", "New / Edit Command", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("CommandDialog", "Command", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("CommandDialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("CommandDialog", "Names", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("CommandDialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("CommandDialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))

