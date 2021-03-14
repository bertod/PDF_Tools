# %%
import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QErrorMessage, QMainWindow, QFileDialog, \
    QAbstractItemView, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit
from GuiHandler.main_gui import Gui
from Plugins.TabPlugin import TabPlugin


class CustomGui(Gui):

    def __init__(self):
        super(CustomGui, self).__init__()
        tab_creator = TabPlugin(self, "TAB NEW CUSTOM")
        new_tab_layout = tab_creator.createTab()
        label2 = QLabel("New Label Widget in Custom Tab.")
        new_tab_layout.addWidget(label2)

        """---- Alternative way of adding tabs without using Plugin ---- """
        """tabnew = QWidget()
        tabnew.layout = QVBoxLayout(tabnew)
        label1 = QLabel("Widget in Tab 1. - external")
        label2 = QLabel("Widget in Tab 2.")
        tabnew.layout.addWidget(label1)
        tabnew.layout.addWidget(label2)
        self.tab_one.addTab(tabnew, "Page1")"""
        """------------------------------------------------------------------"""


"""app = QApplication(sys.argv)
widget = CustomGui()
widget.show()
sys.exit(app.exec_())"""

