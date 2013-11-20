import os

from PySide import QtGui
import EtGui, EtTools

import shared
import webbrowser
import moss

def actionExit_trigger():
    shared.mainWindow.close()

def actionSettings_trigger():
    print "settings"

def fileList_drop(source, event):
    if event.mimeData().hasUrls():
        event.accept()
        files = []
        for url in event.mimeData().urls():
            if url.isLocalFile(): # or is relative
                files.append(url.toLocalFile())
        addFilesToList(source.objectName(), files)

        if source.count() != 0:
            source.findChild(EtGui.EtLabel).hide()
    else:
        event.ignore()
    
def fileList_drag(source, event):
    if event.mimeData().hasUrls():
        event.accept()
    else:
        event.ignore()
    
def addStudentButton_click():
    filePath = QtGui.QFileDialog.getExistingDirectory(None, "Select Student Source Folder to Add Files From", shared.addPath)
    if not filePath == "":
        shared.addPath = os.path.abspath(os.path.join(filePath,".."))
        addFilesToList("studentFileList", [os.path.join(filePath, filename) for filename in os.listdir(filePath)])

        if shared.mainWindow.findChild(QtGui.QCheckBox, "runCheckBox").isChecked():
            runQueryButton_click()

def clearStudentButton_click():
    shared.mainWindow.findChild(EtGui.EtListWidget, "studentFileList").clear()
    shared.mainWindow.findChild(EtGui.EtLabel, "studentDragLabel").show()

def addBaseButton_click():
    filePath = QtGui.QFileDialog.getExistingDirectory(None, "Select Base Source Folder to Add Files From", shared.addPath)
    if not filePath == "":
        shared.addPath = os.path.abspath(os.path.join(filePath,".."))
        addFilesToList("baseFileList", [os.path.join(filePath, filename) for filename in os.listdir(filePath)])

def clearBaseButton_click():
    shared.mainWindow.findChild(EtGui.EtListWidget, "baseFileList").clear()
    shared.mainWindow.findChild(EtGui.EtLabel, "baseDragLabel").show()

def moss_output(message):
    outputMessage(message)

def moss_failed(message):
    outputMessage(message)

def moss_success(message):
    outputMessage("Result: <a href={}>{}</a>".format(message, message))
    outputMessage("Opening result in browser...")
    webbrowser.open(message, new=2)

def runQueryButton_click():
    languageBox =shared.mainWindow.findChild(QtGui.QComboBox, "languageBox")
    language = languageBox.currentText()
    baseFiles = getFilesFromList("baseFileList")
    studentFiles = getFilesFromList("studentFileList")

    client = moss.Client()
    client.OnFailure = moss_failed
    client.OnSuccess = moss_success
    client.Output = moss_output
    client.language = language
    client.RunAsync(studentFiles, baseFiles)

def saveQueryButton_click():
    None

def clearQueryButton_click():
    None

def saveOutputButton_click():
    None

def clearOutputButton_click():
    None

def mainWindow_close(source, event):
    config = shared.config

    fileHandle = open(shared.configPath + shared.configFile, 'w')
    config.set("config","AddFilter", source.findChild(QtGui.QLineEdit, "filterEdit").text())
    config.set("config","IgnoreFilter", source.findChild(QtGui.QLineEdit, "ignoreEdit").text())
    config.set("config", "UseDirectories", source.findChild(QtGui.QCheckBox, "dirCheckBox").isChecked())
    config.set("config", "RunAfterAdd", source.findChild(QtGui.QCheckBox, "runCheckBox").isChecked())
    config.set("config","Language", source.findChild(QtGui.QComboBox, "languageBox").currentText())
    config.set("config","IgnoreCount", source.findChild(QtGui.QSpinBox, "ignoreCountSpinBox").value())
    config.set("config","Comment", source.findChild(QtGui.QLineEdit, "commentEdit").text())
    config.set("config", "AddPath", shared.addPath)
    config.write(fileHandle)
    fileHandle.close()
    event.accept()

def addFilesToList(listName, files):
    fileList = shared.mainWindow.findChild(EtGui.EtListWidget, listName)
    addFilter = shared.mainWindow.findChild(QtGui.QLineEdit, "filterEdit").text()
    ignoreFilter = shared.mainWindow.findChild(QtGui.QLineEdit, "ignoreEdit").text()
    filesAlreadyInList = getFilesFromList(listName)
    sourceFiles = []

    for filename in files:
        sourceFiles.extend(EtTools.getFiles(filename, addFilter, ignoreFilter))

    for filename in sourceFiles:
        if filename not in filesAlreadyInList:
            fileList.addItem(filename)
    
    if fileList.count() != 0:
        fileList.findChild(EtGui.EtLabel).hide()
            
def outputMessage(message):
    textBrowserOutput = shared.mainWindow.findChild(QtGui.QTextBrowser)
    textBrowserOutput.append(message)

def getFilesFromList(listName):
    fileList = shared.mainWindow.findChild(EtGui.EtListWidget, listName)
    files = []
    for i in range(fileList.count()):
        files.append(fileList.item(i).text())

    return files
