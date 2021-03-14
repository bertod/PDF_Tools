# %%
import sys,os
import datetime
import time
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QTimer, QSize, QStringListModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QErrorMessage, QMainWindow, QFileDialog, \
    QAbstractItemView, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.uic import loadUi
from Helpers.HandlerPDF import PDFHandler
from Plugins import *
from PyQt5.QtWidgets import QLabel, QLineEdit
from functools import partial

"""
GUI Widgets:
-- Tab 1 (extract pages)
fileList_two : file upload field
uploadButton :  button for choosing the file (only one) from Windows explorer
remove :
pages : 

-- Tab 2
fileList : file(s) upload area
uploadButton : button for choosing files from Windows explorer
removeAll :
remove :
"""


class Gui(QMainWindow):
    helper_pdf = None
    FORMAT = ".pdf"

    def __init__(self):
        super(Gui, self).__init__()
        self.helper_pdf = PDFHandler()
        loadUi('./UI/gui.ui', self)

        # self.hbox = QHBoxLayout() # inutile?
        # self.centralWidget().setLayout(self.hbox) # inutile?

        self.records_list = []
        self.time_zone_numeric = '+01:00'
        self.setWindowTitle('PDF Handler')
        self.filepath_list = []
        self.filepath_list_two = []
        self.uploadButton.clicked.connect(self.get_files)
        self.outputPathButton_two.clicked.connect(partial(self.browse_output_path, self.outputFilename_two))
        self.outputPathButton.clicked.connect(partial(self.browse_output_path, self.outputFilename))
        self.uploadButton_two.clicked.connect(self.get_single_file)
        self.extractButton.clicked.connect(self.run_extract)
        self.fileList.setAcceptDrops(True)
        self.fileList.setDragEnabled(True)
        self.fileList.setDragDropMode(QAbstractItemView.InternalMove)
        self.mergeButton.clicked.connect(self.run_merge)


    @pyqtSlot()
    def run_extract(self):
        pages_list = self.pagesList.text()

        if len(self.filepath_list_two) == 0:
            self.show_msg_error("Please, upload a PDF!")
            return
        if len(pages_list) == 0:
            self.show_msg_error("Please, insert page ranges!")
            return
        output_filename = self.outputFilename.text()
        if output_filename != "":
            self.helper_pdf.destination_path = output_filename
            # self.helper_pdf.destination_path = self.helper_pdf.OUTPUT_DIR+output_filename+self.FORMAT
        res = self.helper_pdf.extract_pages(self.filepath_list_two[0], pages_list)

        if res == -1:
            self.show_msg_error("Please, check the page range inserted!")
            return
        files_str = "\r\n".join(self.helper_pdf.source_paths)
        details = "Input File: \r\n {} \r\nOutput File: \r\n {}".format(files_str, self.helper_pdf.destination_path)

        self.show_msg_done("Finished. Pages extracted in a new PDF File",
                         details)

    @pyqtSlot()
    def run_merge(self):
        self.filepath_list = [str(self.fileList.item(i).text()) for i in range(self.fileList.count())]
        if len(self.filepath_list) < 2:
            self.show_msg_error("Please, upload at least two PDF files!")
            return
        self.helper_pdf.source_paths = self.filepath_list
        # self.helper_pdf.flush_output()
        output_filename = self.outputFilename_two.text()
        print(output_filename)
        if output_filename != "":
            self.helper_pdf.destination_path = output_filename
            # self.helper_pdf.destination_path = self.helper_pdf.OUTPUT_DIR+output_filename+self.FORMAT
        self.helper_pdf.merge_pdfs()
        files_str = "\r\n".join(self.helper_pdf.source_paths)
        details = "Input File(s): \r\n {} \r\nOutput File: \r\n {}".format(files_str, self.helper_pdf.destination_path)
        self.show_msg_done("Finished. PDF files merged!", details)

    @pyqtSlot()
    def get_single_file(self):
        self.filepath_list_two = self.clear_upload(self.fileList_two,
                                                   self.filepath_list_two)

        fname_single = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.pdf *.txt)")

        filepath = fname_single[0]
        if filepath != '':
            filename = filepath.split("/")[-1]
            self.fileList_two.addItem(filename)
            temp_path = self.helper_pdf.copy_to_temp(filepath, filename)
            self.filepath_list_two.append(temp_path)
        print(self.filepath_list_two)

    @pyqtSlot()
    def get_files(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file',
                                            'c:\\', "Image files (*.pdf *.txt)")

        for filepath in fname[0]:
            filename = filepath.split("/")[-1]
            self.fileList.addItem(filepath)
            # self.fileList.addItem(filename)
            # self.filepath_list.append(filepath)
            temp_path = self.helper_pdf.copy_to_temp(filepath, filename)
            self.filepath_list.append(temp_path)
        self.filepath_list = list(set(self.filepath_list))
        print(self.filepath_list)

    @pyqtSlot()
    def browse_output_path(self, text_obj):
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;PDF Files (*.pdf)")
        # , options = options
        # if fileName:
        #    print(fileName)
        # self.outputFilename_two.setText(fileName)
        text_obj.setText(fileName)

    @pyqtSlot()
    def clear_upload(self, listWidget, uploaded_files_list):
        listWidget.clear()
        self.helper_pdf.flush_temp(uploaded_files_list)
        return []

    @pyqtSlot()
    def show_msg_error(self, error_msg):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        # msg.setSize(QSize(1000, 300));
        msg.setText(error_msg)
        # msg.setInformativeText("Look at anomalies.txt file for checking what I've written")
        msg.setWindowTitle("Error")
        # msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @pyqtSlot()
    def show_msg_done(self, msgtext, details=""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setSize(QSize(1000, 300));
        msg.setText(msgtext)
        # msg.setInformativeText("Look at anomalies.txt file for checking what I've written")
        msg.setWindowTitle("Done")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Ok)
        #msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()

    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.helper_pdf.flush_temp()
            event.accept()
        else:
            event.ignore()


# %%
"""app = QApplication(sys.argv)
widget = Gui()
widget.show()
sys.exit(app.exec_())"""

