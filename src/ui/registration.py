from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFrame, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from src.models.session import Session
from src.ui.app import AppWindow


class RegistrationWindow(QMainWindow):
    def __init__(self, device):
        super(QMainWindow, self).__init__()
        self.device = device
        self.setup_ui()

    def setup_ui(self):
        # Set window size to 800x600
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("BrainBit")
        self.setFixedSize(800, 600)

        # Center the window
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.frameGeometry().width()) // 2
        y = (screen_geometry.height() - self.frameGeometry().height()) // 2
        self.move(x, y)

        self.header = QFrame(self)
        self.header.setGeometry(0, 0, 800, 100)
        palette = self.header.palette()
        palette.setColor(QPalette.Background, QColor("#87CEEB"))
        self.header.setPalette(palette)
        self.header.setAutoFillBackground(True)
        self.header_label = QLabel("Регистрация сессии", self.header)
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
        self.nickname_field = QLineEdit(self)
        self.nickname_field.setGeometry(300, 200, 200, 60)  # Adjust position and size as needed
        self.nickname_field.setPlaceholderText("Никнейм")
        self.nickname_field.setStyleSheet("""
                     QLineEdit {
                         font: 20pt 'Arial';
                         color: #000000;
                         border: none;
                         border-radius: 15px;
                         padding: 10px;
                         min-width: 100px;
                     }
                     QLineEdit:hover {
                         background-color: #C7E4F2;
                     }
                 """)  # Add your CSS-like styles here
        # Set the opacity of the placeholder to 0.5
        palette = self.nickname_field.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(0, 0, 0, 63))  # RGBA color with 0.5 opacity
        self.nickname_field.setPalette(palette)

        # Create a QLineEdit for the "Игра" field
        self.game_field = QLineEdit(self)
        self.game_field.setGeometry(300, 300, 200, 60)  # Adjust position and size as needed
        self.game_field.setPlaceholderText("Игра")
        self.game_field.setStyleSheet("""
                     QLineEdit {
                         font: 20pt 'Arial';
                         color: #000000;
                         border: none;
                         border-radius: 15px;
                         padding: 10px;
                         min-width: 100px;
                     }
                     QLineEdit:hover {
                         background-color: #C7E4F2;
                     }
                 """)  # Add your CSS-like styles here
        # Set the opacity of the placeholder to 0.5
        palette = self.game_field.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(0, 0, 0, 63))  # RGBA color with 0.5 opacity
        self.game_field.setPalette(palette)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setGeometry(300, 400, 200, 60)  # Adjust position and size as needed
        self.submit_button.setStyleSheet("""
                QPushButton {
                    background-color: #C7E4F2;
                    font: 20pt 'Arial';
                    color: #FFFFFF;
                    border: none;
                    border-radius: 15px;
                    padding: 10px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #87CEEB;
                }
            """)  # Add your CSS-like styles here
        self.submit_button.clicked.connect(self.on_submit_button_clicked)

    def on_submit_button_clicked(self):
        # Get the text from the QLineEdit widgets
        nickname = self.nickname_field.text()
        game = self.game_field.text()

        # Assign the text to the corresponding attributes of the session object
        self.session = Session(nickname=nickname, game=game)

        self.app_window = AppWindow(self.session)
        self.app_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = RegistrationWindow(None)
    window.show()
    app.exec_()
