from PyQt5.QtChart import QSplineSeries, QChart, QChartView, QValueAxis
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFrame, QLineEdit, QTabWidget, QTextEdit, \
    QVBoxLayout, QSizePolicy

from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from src.brainbit.reg_signals import RegSignals
from src.models.session import Session


class AppWindow(QMainWindow):
    def __init__(self, session):
        super(QMainWindow, self).__init__()
        self.session = session
        self.setup_ui()

        self.reg_signals_thread = RegSignals(self.session.device)
        self.reg_signals_thread.mental_data_received.connect(self.update_chart)

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
        self.header_label = QLabel(f"Приветствую, {self.session.nickname}", self.header)
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
        """)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(0, 100, 800, 500)  # Adjust position and size as needed
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #87CEEB;
                color: #FFFFFF;
                font: 16pt 'Arial';  # Adjust the font size as needed
                border: none;
                border-radius: 15px;
                padding: 10px;
                min-width: 100px;
                height: 50px;
            }
            QTabBar::tab:selected {
                background-color: #66B2FF;
            }
            QTabBar::tab:hover {
                background-color: #C7E4F2;
            }
        """)

        # Make the tabs expand to fill the available space and prevent text eliding
        self.tab_widget.tabBar().setExpanding(True)
        self.tab_widget.tabBar().setElideMode(Qt.ElideNone)

        # Make the tabs expand to fill the available space
        self.tab_widget.tabBar().setExpanding(True)

        # Create a QTextEdit for the first tab
        self.tab1_content = QTextEdit(self)
        self.tab1_content.setReadOnly(True)  # Make the QTextEdit read-only

        # Add the first tab to the QTabWidget
        self.tab_widget.addTab(self.tab1_content, "Графики")

        # Create the "Начать запись" button
        self.start_button = QPushButton("Начать запись", self)
        self.start_button.setStyleSheet("""
            QPushButton {
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
        self.start_button.clicked.connect(self.start_recording)

        # Create the "Приостоновить" button
        self.pause_button = QPushButton("Приостоновить", self)
        self.pause_button.setStyleSheet("""
            QPushButton {
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
        self.pause_button.clicked.connect(self.pause_recording)

        # Add the buttons to the layout of the first tab

        # self.series = QSplineSeries()
        #
        # # Add data to the series
        # # Replace this with the actual data you want to display
        # self.series.append(0, -6)
        # self.series.append(2, 4)
        # self.series.append(3, 8)
        # self.series.append(7, -4)
        # self.series.append(10, 5)
        #
        # # Create a QChart and add the series to it
        # self.chart = QChart()
        # self.chart.addSeries(self.series)
        #
        # # Create a QValueAxis for the x axis, set its range, and add it to the chart
        # self.x_axis = QValueAxis()
        # self.x_axis.setRange(0, 10)  # Set the range of the x axis to 0-10
        # self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        # self.series.attachAxis(self.x_axis)
        #
        # # Create a QValueAxis for the y axis, set its range, and add it to the chart
        # self.y_axis = QValueAxis()
        # self.y_axis.setRange(-100, 100)  # Set the range of the y axis to 0-10
        # self.chart.addAxis(self.y_axis, Qt.AlignLeft)
        # self.series.attachAxis(self.y_axis)
        #
        # # Create a QChartView to display the chart
        # self.chart_view = QChartView(self.chart)
        #
        # # Enable antialiasing for smoother lines
        # self.chart_view.setRenderHint(QPainter.Antialiasing)
        #
        # # Set the size policy of the QChartView to expanding
        # self.chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.tab1_layout.addWidget(self.chart_view)
        self.tab1_layout.addWidget(self.start_button)
        self.tab1_layout.addWidget(self.pause_button)
        # self.tab1_content.setLayout(self.tab1_layout)

        # Create a QTextEdit for the second tab
        self.tab2_content = QTextEdit(self)
        self.tab2_content.setReadOnly(True)  # Make the QTextEdit read-only

        # Add the second tab to the QTabWidget
        self.tab_widget.addTab(self.tab2_content, "Обратная связь")

        # Create a QTextEdit for the third tab
        self.tab3_content = QTextEdit(self)
        self.tab3_content.setReadOnly(True)  # Make the QTextEdit read-only

        # Add the third tab to the QTabWidget
        self.tab_widget.addTab(self.tab3_content, "Настройки оверлея")