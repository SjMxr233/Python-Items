from Gui.Gui import Gui
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())