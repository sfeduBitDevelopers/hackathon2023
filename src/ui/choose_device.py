from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QApplication, QWidget, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette

from src.ui.check_resistance import CheckResistance

from src.core.log_config import logger


class ChooseDevice(QMainWindow):
    rescan_requested = pyqtSignal()

    def __init__(self, devices):
        super(QMainWindow, self).__init__()
        self.devices = devices
        self.setup_ui()

    def setup_ui(self):
        # Set window size to 800x600
        self.setGeometry(0, 0, 800, 600)

        # Center the window
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.frameGeometry().width()) // 2
        y = (screen_geometry.height() - self.frameGeometry().height()) // 2
        self.move(x, y)

        # Create a header with a soft gray background color and the text "Выберите устройство"
        self.header = QFrame(self)
        self.header.setGeometry(0, 0, 800, 100)
        palette = self.header.palette()
        palette.setColor(QPalette.Background, QColor("#87CEEB"))  # Soft gray color
        self.header.setPalette(palette)
        self.header.setAutoFillBackground(True)
        self.header_label = QLabel("Выберите устройство", self.header)
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

        # Create a new QWidget for the area below the header
        self.content_area = QWidget(self)
        self.content_area.setGeometry(0, 100, 800, 500)  # Adjust the geometry as needed

        # Create a QVBoxLayout to hold the buttons
        layout = QVBoxLayout(self.content_area)

        # Create a button for each device
        for i, device in enumerate(self.devices):
            button = QPushButton(str(device.SerialNumber), self)
            button.setStyleSheet("""
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
            button.clicked.connect(lambda checked, device=device: self.on_button_clicked(device))
            layout.addWidget(button)

        self.rescan_button = QPushButton("Начать поиск заново", self)
        self.rescan_button.setStyleSheet("""
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
                    """)
        self.rescan_button.clicked.connect(self.on_rescan_button_clicked)
        layout.addWidget(self.rescan_button)

        # Set the layout of the content_area to the QVBoxLayout
        self.content_area.setLayout(layout)

    def on_rescan_button_clicked(self):
        self.hide()
        self.rescan_requested.emit()

    def on_button_clicked(self, device):
        # Perform an action with the device
        self.hide()
        self.check_resistance = CheckResistance(device)
        self.check_resistance.show()
