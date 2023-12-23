from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from src.ui.choose_device import ChooseDevice
from src.ui.progress_bar_scan import ProgressBarWindow


class HelloWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        # Set window size to 800x600
        self.setGeometry(0, 0, 800, 600)

        # Center the window
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.frameGeometry().width()) // 2
        y = (screen_geometry.height() - self.frameGeometry().height()) // 2
        self.move(x, y)

        # Create a header with a soft gray background color and the text "Добро пожаловать"
        self.header = QFrame(self)
        self.header.setGeometry(0, 0, 800, 100)
        palette = self.header.palette()
        palette.setColor(QPalette.Background, QColor("#87CEEB"))  # Soft gray color
        self.header.setPalette(palette)
        self.header.setAutoFillBackground(True)
        self.header_label = QLabel("Добро пожаловать", self.header)
        self.header_label.setGeometry(0, 0, 800, 100)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font: 30pt 'Arial';
            color: #FFFFFF;
            font-weight: bold;
            background-color: #87CEEB;
            border-radius: 15px;
            padding: 10px;
            box-shadow: 3px 3px 5px grey;
        """)  # Soft cyan color

        # Add a label in the center of the window with the text "Проверьте подключение bluetooth адаптера и
        # убедитесь, что аккумулятор подключен в ваш BrainBit"
        self.label = QLabel("Проверьте подключение bluetooth адаптера и убедитесь, что аккумулятор подключен в ваш "
                            "BrainBit", self)
        self.label.setGeometry(0, 200, 800, 150)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)  # Enable word-wrapping
        self.label.setStyleSheet("color: #000000; font: 18pt 'Arial'; font-weight: bold; text-align: center;")

        # Add a button at the bottom of the window that, when clicked, will switch to the ChooseDevice window and
        # hide the HelloWindow
        self.push_button = QPushButton('Далее', self)
        self.push_button.setGeometry(350, 500, 100, 50)
        self.push_button.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB;
                font: 20pt 'Arial';
                color: #FFFFFF;
                border: none;
                border-radius: 15px;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #66B2FF;
            }
        """)  # Soft cyan color
        self.push_button.clicked.connect(self.on_next_button_clicked)

    def on_next_button_clicked(self):
        # self.choose_device = ChooseDevice()
        # self.choose_device.show()
        # self.hide()
        self.progress_bar_window = ProgressBarWindow()
        self.progress_bar_window.show()
        self.hide()