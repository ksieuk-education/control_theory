import PyQt6.QtCore as pyqt6_qtcore
import PyQt6.QtGui as pyqt6_gui
import PyQt6.QtWidgets as pyqt6_qtwidgets

import lib.methods.config as methods_config


class ImageViewer(pyqt6_qtwidgets.QLabel):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)

        pixmap = pyqt6_gui.QPixmap(image_path)
        self.setPixmap(pixmap)

        self.resize(pixmap.width(), pixmap.height())
        self.setScaledContents(True)
        size_policy = pyqt6_qtwidgets.QSizePolicy(
            pyqt6_qtwidgets.QSizePolicy.Policy.Expanding, pyqt6_qtwidgets.QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(size_policy)
        self.setMinimumHeight(1)


class CustomWidget(pyqt6_qtwidgets.QWidget):
    def __init__(
        self,
        field_number: int,
        title: str,
        value_name: str,
        value_default: methods_config.FIELD_DEFAULT_TYPE = None,
    ):
        super().__init__()

        self.label = pyqt6_qtwidgets.QLabel()
        self.label.setText(title)
        self.label.setToolTip(value_name)
        self.label.setObjectName(f"label_input_{field_number}")
        self.label.setAlignment(pyqt6_qtcore.Qt.AlignmentFlag.AlignHCenter)
        size_policy = pyqt6_qtwidgets.QSizePolicy(
            pyqt6_qtwidgets.QSizePolicy.Policy.Expanding, pyqt6_qtwidgets.QSizePolicy.Policy.Expanding
        )
        self.label.setSizePolicy(size_policy)

        self.lineEdit = pyqt6_qtwidgets.QLineEdit()
        self.lineEdit.setObjectName(f"le_input_{field_number}")
        self.lineEdit.setSizePolicy(size_policy)
        if value_default is not None:
            self.lineEdit.setText(str(value_default))

        layout = pyqt6_qtwidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(pyqt6_qtcore.Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.label, 1)
        layout.addWidget(self.lineEdit, 0, alignment=pyqt6_qtcore.Qt.AlignmentFlag.AlignRight)

    def text(self):
        return self.label.toolTip(), self.lineEdit.text()
