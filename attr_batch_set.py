import os
import tempfile
from PySide2 import QtWidgets

import maya.mel as mel
import pymel.core as pm


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

        self.tmp_file = self.get_tmp_file()
        self.store_history()

    def build_ui(self):
        widgets = (self.name_label, self.name_input, self.pick_bt)
        map(lambda widget: self.pick_la.addWidget(widget), widgets)
        self.layout.addLayout(self.pick_la)
        self.layout.addWidget(self.run_bt)

    def connect_cmd(self):
        self.pick_bt.clicked.connect(self.pick_cmd)
        self.run_bt.clicked.connect(self.set_attr)

    def pick_cmd(self):
        print self.tmp_file
        attr_name = self.get_attr_name()
        if attr_name:
            self.name_label.setText(attr_name)

    def store_history(self):
        mel.eval('scriptEditorInfo -historyFilename "{0}" -writeHistory true;'.format(self.tmp_file))

    def get_attr_name(self):
        with open(self.tmp_file, 'r') as f:
            history = f.readlines()

        line_set_attr = filter(lambda line: line.startswith('setAttr'), history)
        if not line_set_attr:
            return
        try:
            attr_name = line_set_attr[-1].split('.')[-1].split()[0].strip()
            attr_name = filter(str.isalpha, attr_name)
            return attr_name
        except IndexError:
            return

    def set_attr(self):
        attr_name = self.name_label.text()
        value = self.name_input.text()
        for node in pm.ls(sl=True):
            v = node.getShape().attr(attr_name).get()
            if isinstance(v, str):
                value = str(value)
            elif isinstance(v, int):
                value = int(value)
            elif isinstance(v, float):
                value = float(v)
            node.getShape().setAttr(attr_name, value)

    @staticmethod
    def get_tmp_file():
        return os.path.join(tempfile.gettempdir(), 'tempHistoryLog.txt')


def main():
    global local
    local = MayaAttrBatchSet()
    local.show()
