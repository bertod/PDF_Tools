from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout


class TabPlugin:
    def __init__(self, mainGui, tabName):
        self.mainGui = mainGui
        self.tabName = tabName

    def createTab(self):
        tabnew = QWidget()
        tabnew.layout = QVBoxLayout(tabnew)
        """label1 = QLabel("Widget in Tab {}".format(self.tabName))
        label2 = QLabel("Widget in Tab 2.")
        tabnew.layout.addWidget(label1)
        tabnew.layout.addWidget(label2)"""
        self.mainGui.tab_one.addTab(tabnew, self.tabName)
        return tabnew.layout


