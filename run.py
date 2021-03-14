import sys
from PyQt5.QtWidgets import QApplication
from GuiHandler import main_gui, custom_gui

app = QApplication(sys.argv)
widget = custom_gui.CustomGui()
widget.show()
sys.exit(app.exec_())