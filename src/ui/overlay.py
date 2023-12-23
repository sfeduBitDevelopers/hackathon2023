from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Убрать рамку вокруг окна
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Включить использование OpenGL
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Установить размер окна
        self.resize(200, 200)

        # Получить разрешение экрана
        screen_geometry = QApplication.desktop().availableGeometry()

        # Переместить окно в правый нижний угол
        self.move(screen_geometry.width() - self.width(), screen_geometry.height() - self.height())

        # Добавить виджет для отображения контента
        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Добавить виджет с текстом в центр окна
        label = QLabel("We are here", content_widget)
        label.setStyleSheet("color: white; font-size: 20px;")
        content_layout.addWidget(label)

        self.setCentralWidget(content_widget)

        # Сделать окно поверх всех окон
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.fillRect(event.rect(), QBrush(Qt.transparent))


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
