import os
import tempfile
from PySide2 import QtWidgets
import maya.cmds as cmds
import maya.mel as mel


class MayaAttrBatchSet(QtWidgets.QWidget):

    def __init__(self):
        super(MayaAttrBatchSet, self).__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.pick_la = QtWidgets.QHBoxLayout()
        self.name_label = QtWidgets.QLabel('{name}')
        self.name_input = QtWidgets.QLineEdit()
        self.pick_bt = QtWidgets.QPushButton('Pick')
        self.run_bt = QtWidgets.QPushButton('Run')
        self.build_ui()
        self.connect_cmd()
        self.setLayout(self.layout)

    def build_ui(self):
        widgets = (self.name_label, self.name_input, self.pick_bt)
        map(lambda widget: self.pick_la.addWidget(widget), widgets)
        self.layout.addLayout(self.pick_la)
        self.layout.addWidget(self.run_bt)

    def connect_cmd(self):
        self.pick_bt.clicked.connect(self.pick_cmd)

    def pick_cmd(self):
        attr_name = self.get_attr_name()

    def get_attr_name(self):
        tmp_file = os.path.join(tempfile.gettempdir(), 'tempHistoryLog.txt')



def main():
    global local
    local = MayaAttrBatchSet()
    local.show()
