from PySide.QtGui import QWidget, QVBoxLayout, QGridLayout

__author__ = 'lazToum'


class Reports(QWidget):
    def __init__(self):
        self.associations_file = "./associations.csv"
        QWidget.__init__(self)
        self.setMinimumWidth(600)
        self.layout = QVBoxLayout()
        # Create the QVBoxLayout that lays out the whole form
        self.grid_layout = QGridLayout()

    def run(self):
        self.show()
