from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QProgressBar, QApplication, QLabel, QFrame, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

from src.brainbit.connect import ScanDevices
from src.ui.choose_device import ChooseDevice
from src.core.log_config import logger


def scaner():
    scan = ScanDevices()
    devices = scan.scan()
    return devices


class ScanThread(QThread):
    scan_finished = pyqtSignal(object)

    def run(self):
        sensor = scaner()
        self.scan_finished.emit(sensor)


class ProgressBarWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.devices = None
        self.setup_ui()

    def start_pr_bar(self):
        # Create a QTimer to update the progress bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(50)  # Update the progress bar every 100 ms

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

        # Create a header with a soft gray background color and the text "Поиск устройства"
        self.header = QFrame(self)
        self.header.setGeometry(0, 0, 800, 100)
        palette = self.header.palette()
        palette.setColor(QPalette.Background, QColor("#87CEEB"))  # Soft gray color
        self.header.setPalette(palette)
        self.header.setAutoFillBackground(True)
        self.header_label = QLabel("Поиск устройства", self.header)
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

        # Create a QProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(200, 250, 400, 75)  # Adjust the geometry as needed
        self.progress_bar.setRange(0, 100)  # Set the range of the progress bar to 0-100
        self.progress_bar.setValue(0)  # Set the initial value of the progress bar to 0
        self.progress_bar.setTextVisible(False)  # Hide the text
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #87CEEB;
                color: #aaaaaa;
                background-color: #aaaaaa;
                border-radius: 5px;
                text-align: center;
                font: 20pt 'Arial';
            }
            QProgressBar::chunk {
                background-color: #87CEEB;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setAlignment(Qt.AlignCenter)  # Align the text in the center of the progress bar

        self.start_pr_bar()

        # Scan for devices
        self.scan_thread = ScanThread()
        self.scan_thread.scan_finished.connect(self.on_scan_finished)
        self.scan_thread.start()

    def on_scan_finished(self, devices):
        if devices == 'No devices':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Устройства не были найдены. Повторить поиск?")
            msg.setWindowTitle("No Devices Found")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                msg.done(QMessageBox.Ok)
                self.progress_bar.setValue(0)
                self.start_pr_bar()
                # If the user clicked "OK", start scanning again
                self.scan_thread.start()
            else:
                # If the user clicked "Cancel", exit the program
                QApplication.quit()
        else:
            self.devices = devices
            logger.info(self.devices)
            self.choose_device = ChooseDevice(self.devices)
            self.choose_device.rescan_requested.connect(self.restart_scan)
            self.choose_device.show()
            self.hide()

    def restart_scan(self):
        self.hide()
        self.new_scan_window = ProgressBarWindow()
        self.new_scan_window.show()

    def update_progress_bar(self):
        # Increase the value of the progress bar by 1
        self.progress_bar.setValue(self.progress_bar.value() + 1)
        # Stop the timer when the progress bar is full
        if self.progress_bar.value() == 100:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication([])
    window = ProgressBarWindow()
    window.show()
    app.exec_()
