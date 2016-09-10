#!/usr/bin/env python
import sys
from qt import *

a = QApplication(sys.argv)

hello=QLabel("hello world!",None)

a.setMainWidget(hello)

hello.show()

a.exec_loop()

