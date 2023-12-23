from PyQt5.QtWidgets import QApplication
from src.ui.hello_window import HelloWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = HelloWindow()
    main_window.show()
    sys.exit(app.exec_())
