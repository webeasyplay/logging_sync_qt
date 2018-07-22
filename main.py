import sys
from PySide2.QtWidgets import QApplication,QWidget, QPushButton, QTextEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import PySide2.QtGui
import logging


write = None

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers = [logging.FileHandler('my.log', 'w', 'utf-8'),])

class MyNewHandler(logging.Handler):

    write = None

    def __init__(self, write_method):
        logging.Handler.__init__(self)
        self.write = write_method

    def emit(self, record):
        self.write(record.message + "\r\n")


class MyWidget(QWidget):

    window = ...  # type: QObject

    def __init__(self, ui_file, parent=None):
        super(MyWidget, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)

        ui_file.close()
        add_click_btn = self.window.findChild(QPushButton, 'ADD_BTN')
        add_click_btn.clicked.connect(self.add_click_handler)

        # log 控件設定
        self.edit = self.window.findChild(QTextEdit, 'out_log')
        self.out = None

        self.window.show()

    def add_click_handler(self):
        logging.info("ADD MESSAGE")

    def write(self, m):
        self.edit.moveCursor(PySide2.QtGui.QTextCursor.End)
        self.edit.insertPlainText(m)
        if self.out:
            self.out.write(m)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = MyWidget('mainqt.ui')
    console = MyNewHandler(app_window.write)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    sys.exit(app.exec_())