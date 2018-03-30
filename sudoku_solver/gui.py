import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class SudokuWidget(QWidget):
    def __init__(self, parent=None):
        super(SudokuWidget, self).__init__(parent)

        layout = QVBoxLayout()

        self.placeholder = QLabel("Puzzle")
        self.placeholder.setMinimumSize(500, 500)
        self.placeholder.setStyleSheet("border: 1px solid black")
        self.placeholder.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.placeholder)
        self.setLayout(layout)


class SudokuDialog(QDialog):
    def __init__(self, parent=None):
        super(SudokuDialog, self).__init__(parent)

        layout = QHBoxLayout()
        self.puzzle = SudokuWidget()
        layout.addWidget(self.puzzle)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(QPushButton("solve"))
        buttonLayout.addWidget(QPushButton("clear"))
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.setFixedSize(700, 600)
        self.puzzle.setFocus()

        self.show()

def main():
    app = QApplication([])
    gui = SudokuDialog()
    sys.exit(app.exec_())
