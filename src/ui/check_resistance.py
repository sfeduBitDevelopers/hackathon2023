import os

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QThread, pyqtSignal, QEasingCurve
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QWidget, QVBoxLayout, QSizePolicy, QPushButton
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtSvg import QSvgWidget
from time import sleep

from src.core.log_config import logger
from src.brainbit.check_resistance import BrainbitCheckResistance
from src.ui.registration import RegistrationWindow


def resist(device):
    brainbit_check_resistance = BrainbitCheckResistance(device)
    brainbit_check_resistance.check_resistance()
    return brainbit_check_resistance


class ResistChecked(QThread):
    resist_finished = pyqtSignal(object)

    def __init__(self, device):
        super(QThread, self).__init__()
        self.device = device

    def run(self):
        brainbit_check_resistance = resist(self.device)
        self.resist_finished.emit(brainbit_check_resistance)


class CheckResistance(QMainWindow):

    def __init__(self, device):
        super(QMainWindow, self).__init__()
        self.animations = []
        self.device = device
        self.setup_ui()
        self.show()

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

        # Create a QVBoxLayout to hold the SVG image
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a header with a soft gray background color and the text "Проверка электродов"
        self.header = QLabel("Проверка электродов")
        self.header.setFixedHeight(100)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("""
            font: 30pt 'Arial';
            color: #FFFFFF;
            font-weight: bold;
            background-color: #87CEEB;
            box-shadow: 3px 3px 5px grey;
        """)  # Soft cyan color

        # Add the header to the layout
        layout.addWidget(self.header)

        # Create a QSvgWidget with the path to your SVG file
        brainbit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', 'BrainBit.svg'))
        svg_widget = QSvgWidget(brainbit_path)

        # Scale the SVG image
        svg_renderer = svg_widget.renderer()
        svg_renderer.setViewBox(QtCore.QRectF(430, 250, 1100, 1100))

        # Add the QSvgWidget to your layout
        layout.addWidget(svg_widget)

        # Create a QWidget as the main container and set the layout
        main_container = QWidget()
        main_container.setLayout(layout)

        # Set the main container as the central widget
        self.setCentralWidget(main_container)

        # Load SVG images
        x_svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', 'x.svg'))
        check_svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'icons', 'check.svg'))

        # Create and position the 'x' and 'check' icons
        self.x_icons = []
        self.check_icons = []
        for i in range(4):
            x_icon = QSvgWidget(x_svg_path)
            x_icon.renderer().setViewBox(QRect(0, 0, 24, 24))
            x_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            x_icon.setFixedSize(35, 35)
            if i < 2:
                x_icon.move(65 + i * 110, 400)  # Adjust position as needed
            else:
                x_icon.move(365 + i * 110, 400)
            x_icon.setParent(self)  # Add the 'x' icon to the main window
            self.x_icons.append(x_icon)

            check_icon = QSvgWidget(check_svg_path)
            check_icon.renderer().setViewBox(QRect(0, 0, 24, 24))
            check_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            check_icon.setFixedSize(35, 35)
            if i < 2:
                check_icon.move(65 + i * 110, 400)
            else:
                check_icon.move(365 + i * 110, 400)
            check_icon.hide()
            check_icon.setParent(self)  # Add the 'check' icon to the main window
            self.check_icons.append(check_icon)

        self.check_resistance()

    def check_resistance(self):
        self.scan_thread = ResistChecked(self.device)
        self.scan_thread.resist_finished.connect(self.on_resist_finished)
        self.scan_thread.start()

    def on_resist_finished(self, brainbit_check_resistance):
        self.brainbit_check_resistance = brainbit_check_resistance
        resistance = brainbit_check_resistance.resistance
        bad_connection_detected = False
        for i in range(4):
            # Determine the sensor name based on the icon index
            sensor_name = ["O1", "T3", "T4", "O2"][i]

            try:
                # Animate the transition if the resistance is lower than 2*10^6
                if resistance[sensor_name][-1] < 2 * 10 ** 6:
                    logger.info(f"Resistance for {sensor_name} is good")
                    self.x_icon = self.x_icons[i]
                    self.check_icon = self.check_icons[i]

                    self.animation1 = QPropertyAnimation(self.x_icon, b"opacity")
                    self.animation1.setDuration(1000)
                    self.animation1.setStartValue(1.0)
                    self.animation1.setEndValue(0.0)

                    self.animation2 = QPropertyAnimation(self.check_icon, b"opacity")
                    self.animation2.setDuration(1000)
                    self.animation2.setStartValue(0.0)
                    self.animation2.setEndValue(1.0)

                    # Start the second animation when the first animation finishes
                    self.animation1.finished.connect(self.animation2.start)

                    # Hide the 'x' icon and show the 'check' icon when the second animation finishes
                    self.animation2.finished.connect(self.x_icon.hide)
                    self.animation2.finished.connect(self.check_icon.show)

                    # Start the first animation
                    self.animation1.start()

                    # Store the QPropertyAnimation objects as instance variables
                    self.animations.append(self.animation1)
                    self.animations.append(self.animation2)
                else:
                    logger.info(f"Bad connection for {sensor_name}")
                    bad_connection_detected = True
            except Exception as e:
                logger.error(f"Error occurred while checking resistance for {sensor_name} {e}")

        # If a bad connection was detected, start the resistance check again
        if bad_connection_detected:
            self.check_resistance()
        else:
            # Create the button to open the other window
            self.other_window_button = QPushButton("Далее", self)
            self.other_window_button.setGeometry(350, 500, 100, 50)
            self.other_window_button.setStyleSheet("""
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
                """)  # Add your CSS-like styles here
            self.other_window_button.clicked.connect(self.on_other_window_button_clicked)

            # Add the QPushButton to the layout
            self.layout().addWidget(self.other_window_button)

            # Hide the button initially
            self.other_window_button.hide()

            # Create a QPropertyAnimation to animate the button's opacity
            self.button_animation = QPropertyAnimation(self.other_window_button, b"windowOpacity")
            self.button_animation.setDuration(1000)  # Duration of 1 second
            self.button_animation.setStartValue(0.0)  # Start from fully transparent
            self.button_animation.setEndValue(1.0)  # End at fully opaque
            self.button_animation.setEasingCurve(
                QEasingCurve.InOutQuad)  # Use an easing curve for a more natural animation

            # Show the button and start the animation when the last check icon animation finishes
            self.animation2.finished.connect(self.other_window_button.show)
            self.animation2.finished.connect(self.button_animation.start)

    def on_other_window_button_clicked(self):
        # Open the other window
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication([])
    window = CheckResistance(None)
    window.show()
    app.exec_()
