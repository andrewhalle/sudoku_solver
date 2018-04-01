import sys
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from .sudoku import Sudoku

class SudokuWidget(QWidget):
    def __init__(self, parent=None):
        super(SudokuWidget, self).__init__(parent)
        self.sudoku = Sudoku()
        self.focus_square = (0, 0)
        self.setFixedSize(500, 500)
        self.setFocusPolicy(Qt.ClickFocus)

    def solve(self):
        self.sudoku.solve()
        self.update()

    def clear(self):
        self.sudoku = Sudoku()
        self.update()

    def enter(self, value):
        i = self.focus_square[0]
        j = self.focus_square[1]
        if value < 0 or value > 9:
            raise ValueError("that's not a valid sudoku value")
        self.sudoku.data[i][j] = value

    def moveFocusSquare(self, new_focus_square):
        if not isinstance(new_focus_square, tuple) or len(new_focus_square) != 2:
            raise ValueError("new focus square must be 2x2 tuple")
        if new_focus_square[0] < 0 or new_focus_square[0] > 8 or new_focus_square[1] < 0 or new_focus_square[1] > 8:
            raise ValueError("index out of bounds")
        self.focus_square = new_focus_square

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            if self.focus_square[0] == 8:
                return
            self.moveFocusSquare((self.focus_square[0] + 1, self.focus_square[1]))
            self.update()
        elif event.key() == Qt.Key_Left:
            if self.focus_square[0] == 0:
                return
            self.moveFocusSquare((self.focus_square[0] - 1, self.focus_square[1]))
            self.update()
        elif event.key() == Qt.Key_Up:
            if self.focus_square[1] == 0:
                return
            self.moveFocusSquare((self.focus_square[0], self.focus_square[1] - 1))
            self.update()
        elif event.key() == Qt.Key_Down:
            if self.focus_square[1] == 8:
                return
            self.moveFocusSquare((self.focus_square[0], self.focus_square[1] + 1))
            self.update()
        elif event.text() in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            num = int(event.text())
            self.enter(num)
            self.update()
        elif event.key() == Qt.Key_Backspace:
            self.enter(0)
            self.update()

    def paintEvent(self, event):
        row_width = self.width() / 9
        white = QColor(255, 255, 255)
        black = QColor(0, 0, 0)
        blue = QColor(0, 0, 255)
        linePen = QPen(black)
        thickPen = QPen(black)
        thickPen.setWidth(2)
        bluePen = QPen(blue)
        bluePen.setWidth(2)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(0, 0)
        
        painter.setPen(thickPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawConvexPolygon(QPoint(0, 0), QPoint(0, self.height()), QPoint(self.width(), self.height()), QPoint(self.width(), 0))
        painter.setPen(linePen)
        for i in range(8):
            x = (i + 1) * row_width
            y = (i + 1) * row_width
            if i in [2, 5]:
                painter.setPen(thickPen)
            painter.drawLine(x, 0, x, self.height())
            painter.drawLine(0, y, self.width(), y)
            if i in [2, 5]:
                painter.setPen(linePen)
        painter.setPen(bluePen)
        x1 = (row_width * self.focus_square[0])
        x2 = (row_width * (self.focus_square[0] + 1))
        y1 = (row_width * self.focus_square[1])
        y2 = (row_width * (self.focus_square[1] + 1))
        painter.drawConvexPolygon(QPoint(x1, y1), QPoint(x1, y2), QPoint(x2, y2), QPoint(x2, y1))

        painter.setPen(linePen)
        painter.setFont(QFont("Arial", pointSize=20, weight=QFont.Normal))
        for i in range(9):
            for j in range(9):
                if self.sudoku.data[i][j] != 0:
                    painter.drawText(row_width * i, row_width * j, row_width, row_width, Qt.AlignCenter, str(self.sudoku.data[i][j]))


class SudokuDialog(QDialog):
    def __init__(self, parent=None):
        super(SudokuDialog, self).__init__(parent)

        layout = QHBoxLayout()
        self.puzzle = SudokuWidget()
        layout.addWidget(self.puzzle)

        buttonLayout = QVBoxLayout()
        self.solve_button = QPushButton("solve")
        self.clear_button = QPushButton("clear")
        self.solve_button.clicked.connect(self.puzzle.solve)
        self.clear_button.clicked.connect(self.puzzle.clear)
        buttonLayout.addWidget(self.solve_button)
        buttonLayout.addWidget(self.clear_button)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.setFixedSize(650, 600)
        self.puzzle.setFocus()

        self.setWindowTitle("Sudoku Solver")

        self.show()

def main():
    app = QApplication([])
    gui = SudokuDialog()
    sys.exit(app.exec_())
