# -*- encoding:utf-8 -*-

#运行入口

import sys

from PyQt5 import QtWidgets
from PyQt5 import sip
from Main_Function import fun_main

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = fun_main()
    ui.show()
    sys.exit(app.exec_())

