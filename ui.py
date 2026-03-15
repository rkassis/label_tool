import PySide6.QtWidgets

import maya.cmds

import label_tool.joint


class LabelUI(PySide6.QtWidgets.QWidget):
    """Label UI to set labels on selected joints.

    To use it directly in the script editor:

    import sys
    import importlib

    tool_path = '<your tool path here>'

    if tool_path not in sys.path:
        sys.path.append(tool_path)

    import label_tool.ui

    # This is not necessary if you're currently not doing changes on the tool
    importlib.reload(label_tool.ui)

    label_ui = label_tool.ui.LabelUI()
    label_ui.show()
    """

    def __init__(self, *args, **kwargs):
        """Initialize Label UI.
        """
        super().__init__(*args, **kwargs)

        self.pattern_label = PySide6.QtWidgets.QLabel('Pattern to remove: ')
        self.pattern_line_edit = PySide6.QtWidgets.QLineEdit()

        self.pattern_layout = PySide6.QtWidgets.QHBoxLayout()
        self.pattern_layout.addWidget(self.pattern_label)
        self.pattern_layout.addWidget(self.pattern_line_edit)

        self.side_label = PySide6.QtWidgets.QLabel('Side: ')
        self.side_combo_box = PySide6.QtWidgets.QComboBox()

        # SIDE_DICT =  {'center': 0, 'left': 1, 'right': 2}
        for side in label_tool.joint.Joint.SIDE_DICT.keys():
            self.side_combo_box.addItem(side)

        self.side_layout = PySide6.QtWidgets.QHBoxLayout()

        self.side_layout.addWidget(self.side_label)
        self.side_layout.addWidget(self.side_combo_box)

        self.set_label_button = PySide6.QtWidgets.QPushButton('Set Label')
        self.set_label_button.clicked.connect(self.__set_label)

        self.layout = PySide6.QtWidgets.QVBoxLayout()

        self.setLayout(self.layout)

        self.layout.addLayout(self.pattern_layout)
        self.layout.addLayout(self.side_layout)
        self.layout.addWidget(self.set_label_button)

    def __set_label(self):

        for joint in maya.cmds.ls(selection=True, type='joint'):
            my_joint = label_tool.joint.Joint(name=joint,
                                              side=self.side_combo_box.currentText(),
                                              pattern=self.pattern_line_edit.text())

            my_joint.set_label()
