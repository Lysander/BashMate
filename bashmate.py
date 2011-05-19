#!/usr/bin/env python2
# coding: utf-8

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""
    ~~~~~~~~~~
    Bashfriend
    ~~~~~~~~~~
    
    Simnple Tool to manage Snippets / Templates for Shell Commands.
    Those Templates can be filled with values via a GUI.
"""

import sys
import json
#import re
from operator import itemgetter

from PyQt4.QtGui import (QMainWindow, QApplication, QPushButton, QDialog,
                         QStringListModel, QFileDialog, QSortFilterProxyModel,
                         QMessageBox)
from PyQt4.QtCore import (Qt, QAbstractTableModel, QVariant, QModelIndex,
                          QRegExp)

from ui_mainwindow import Ui_MainWindow
from ui_commanddialog import Ui_CommandDialog

import icons_rc


FILENAME = r"commands.json"
FIELDNAME = itemgetter(1)


class CommandTemplate(object):
    
    def __init__(self, command, info="", names=[]):
        self.command = command
        self.info = info
        self.names = names
    
    def __repr__(self):
        return "<CommandTemplate({0})>".format(self.command)
    
    def render(self, **kwargs):          
        return self.command.format(**kwargs)


class CommandTemplateEncoder(json.JSONEncoder):
    """
    JSON hook-class to serialize aCommandTemplate object
    """
    
    def default(self, obj):
        if isinstance(obj, CommandTemplate):
            return {
                "command": obj.command,
                "info": obj.info,
                "names": obj.names
            }
        return json.JSONEncoder.default(self, obj)


class CommandModel(QAbstractTableModel):
    def __init__(self, commands, parent=None):
        QAbstractTableModel.__init__(self)
        self.commands = commands

    def rowCount(self, parent=None):
        return len(self.commands)
    
    def columnCount(self, parent=None):
        return 2

    def data(self, index, role):
        command = self.currentCommand(index)
        if role == Qt.DisplayRole:
            if  index.column() == 0:
                return command.command
            elif  index.column() == 1:
                return command.info
    
    def addCommand(self, command):
        index = self.createIndex(self.rowCount(), 0)
        self.beginInsertRows(QModelIndex(), index.row(), index.row())
        self.commands.append(command)
        self.insertRows(index.row(), 1)
        self.dataChanged.emit(index, index)
        self.endInsertRows()
    
    def removeCommand(self, index):
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        self.commands.pop(index.row())
        self.dataChanged.emit(index, index)
        self.endRemoveRows()
    
    def currentCommand(self, index):
        return self.commands[index.row()] if index.row() > -1 else None
           
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(["Command", "Info"][section])


class BindModel(QAbstractTableModel):
    def __init__(self, command, parent=None):
        QAbstractTableModel.__init__(self)
        self.names = command.names
        self.bindings = dict.fromkeys(self.names)

    def rowCount(self, parent=None):
        return len(self.names)
    
    def columnCount(self, parent=None):
        return 2

    def data(self, index, role):
        name = self.currentName(index)
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return name
            elif  index.column() == 1:
                return self.bindings[name]
          
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and index.column() == 1 and role == Qt.EditRole:
            name = self.currentName(index)
            self.bindings[name] = value.toString()
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def currentName(self, index):
        return self.names[index.row()]

    def flags(self, index):
        return (
            Qt.ItemIsEnabled |
            Qt.ItemIsSelectable |
            Qt.ItemIsEditable
        )
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(["Name", "Value"][section])


class CommandDialog(QDialog):
    
    def __init__(self, command=None, parent=None):
        QDialog.__init__(self)
        self.ui = Ui_CommandDialog()
        self.ui.setupUi(self)
        
        self.ui.namesView.setModel(QStringListModel(self))
        
        self.ui.commandEdit.textChanged.connect(self.parseNames)
        #self.ui.nameEdit.textChanged.connect(self.activate)
        #self.ui.addButton.clicked.connect(self.addName)
        #self.ui.deleteButton.clicked.connect(self.deleteName)
        self.ui.deleteButton.setVisible(False)
        self.ui.addButton.setVisible(False)
        self.ui.nameEdit.setVisible(False)
        
        if command:
            self.ui.commandEdit.setText(command.command)
            self.ui.infoEdit.setText(command.info)
        
    @property
    def command(self):
        return CommandTemplate(unicode(self.ui.commandEdit.text()), 
                               unicode(self.ui.infoEdit.toPlainText()),
                               map(unicode, self.ui.namesView.model().\
                                        stringList()))
    
    #def activate(self, text):
        #state = False
        #if len(text) > 0:
            #state = True
        #self.ui.addButton.setEnabled(state)
        #self.ui.deleteButton.setEnabled(state)
    
    #def addName(self):
        #model = self.ui.namesView.model()
        #model.insertRows(0, 1)
        #model.setData(model.createIndex(0, 0), QVariant(
                #self.ui.nameEdit.text()))
        
    #def deleteName(self):
        #model = self.ui.namesView.model()
        #model.removeRows(self.ui.namesView.currentIndex().row(), 1)
    
    def parseNames(self, text):
        try:
            names = [FIELDNAME(token) for token in unicode(text).\
                    _formatter_parser() if FIELDNAME(token) is not None]
        # einzelne "{" oder "}"; beim Tippen tritt das logischer Weise auf
        except ValueError:
            pass
        else:
            # doppelte Einträge elemenieren
            #self.ui.namesView.model().setStringList(list(set(map(unicode,            
                    #self.ui.namesView.model().stringList())) | set(names)))
            self.ui.namesView.model().setStringList(list(set(names)))


class MainWindow(QMainWindow):
    
    def __init__(self, filename=None, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        if filename is not None:
            self.initCommandModel(load_commands(filename))
        else:
            self.initCommandModel([])
        
        self.ui.action_Load.triggered.connect(self.loadCommands)
        self.ui.action_Save.triggered.connect(self.saveCommands)
        
        self.ui.action_Add.triggered.connect(self.addCommand)
        self.ui.action_Edit.triggered.connect(self.editCommand)
        self.ui.action_Remove.triggered.connect(self.removeCommand)
        self.ui.action_Apply.triggered.connect(self.render)
        
        self.ui.action_About_BashMate.triggered.connect(self.about)
        
        self.ui.commandView.activated.connect(self.changeDetailsView)
        self.ui.applyButton.clicked.connect(self.render)
        self.ui.filterEdit.textChanged.connect(self.filter_changed)
        #self.ui.addButton.clicked.connect(self.addCommand)
        #self.ui.editButton.clicked.connect(self.editCommand)
        #self.ui.removeButton.clicked.connect(self.removeCommand)
        #self.ui.commandView.model().dataChanged.connect(self.change)
        #self.ui.commandView.activated.connect(self.activate)
    
    def initCommandModel(self, commands=[]):
        self.cmdmodel = CommandModel(commands, self)
        proxymodel= QSortFilterProxyModel(self)
        proxymodel.setSourceModel(self.cmdmodel)
        proxymodel.setFilterKeyColumn(1)
        self.ui.commandView.setModel(proxymodel)
        
    def loadCommands(self):
        filename = unicode(QFileDialog.getOpenFileName(self, 
                            u"Load CommandTemplate File", ".",
                            u"CommandTemplate File (*.json)"))
        self.initCommandModel(load_commands(filename))
    
    def saveCommands(self):
        filename = unicode(QFileDialog.getSaveFileName(self, 
                            u"Save CommandTemplate File", ".",
                            u"CommandTemplate File (*.json)"))
        dump_commands(self.cmdmodel.commands, filename)
    

    def changeDetailsView(self, index):
        command = self.cmdmodel.currentCommand(index)
        self.ui.commandBrowser.setText(command.command)
        self.ui.infoBrowser.setText(command.info)
        self.ui.bindView.setModel(BindModel(command, self))
    
    def render(self):
        command = self.cmdmodel.currentCommand(
                self.ui.commandView.currentIndex())
        bindings = self.ui.bindView.model().bindings
        self.ui.cmdEdit.setText(command.render(**bindings))
        
    def addCommand(self):
        dialog = CommandDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.cmdmodel.addCommand(dialog.command)

    def editCommand(self):
        command = self.cmdmodel.currentCommand(
                self.ui.commandView.currentIndex())
        dialog = CommandDialog(command, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            commands = self.cmdmodel.commands
            commands[commands.index(command)] = dialog.command

    def removeCommand(self):
        self.cmdmodel.removeCommand(self.ui.commandView.currentIndex())

    def filter_changed(self, pattern):
        regExp = QRegExp(pattern, Qt.CaseInsensitive)
        self.ui.commandView.model().setFilterRegExp(regExp)

    def change(self, left, right):
        print self.ui.commandView.currentIndex().row()
        self.changeDetailsView(self.ui.commandView.currentIndex())
        
    def about(self):
       box = QMessageBox()
       box.setText(u"BashMate - the beginner firendly Shell Snippet Manager")
       box.setInformativeText(
            u"(c) 2011 by Christian Hausknecht <christian.hausknecht@gmx.de>")
       box.exec_()


def load_commands(filename):
    commands = []
    with open(filename, "r") as infile:
        data = json.load(infile)
    for command in data:
        commands.append(CommandTemplate(command["command"], command["info"],
                                        command["names"]))
    return commands
    

def dump_commands(commands, filename):
    with open(filename, "w") as outfile:
        data = json.dump(commands, outfile, indent=4, 
                         cls=CommandTemplateEncoder)
    
    
if __name__ == "__main__":
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    app = QApplication(sys.argv)
    widget = MainWindow(filename) if filename is not None else MainWindow()
    widget.show()
    sys.exit(app.exec_())
