from PyQt5.QtChart import QSplineSeries, QChart, QChartView, QValueAxis
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QFrame, QLineEdit, QTabWidget, QTextEdit, \
    QVBoxLayout, QSizePolicy, QWidget

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

        # Add the buttons to the layout of the first tab

        self.series = QSplineSeries()

        # Add data to the series
        # Replace this with the actual data you want to display
        self.series.append(0, -24)
        self.series.append(1, -12)
        self.series.append(2, -27)
        self.series.append(3, -22)
        self.series.append(4, -15)
        self.series.append(5, -30)
        self.series.append(6, -15)
        self.series.append(7, 27)
        self.series.append(8, -12)
        self.series.append(9, -15)
        self.series.append(10, -9)

        # Create a QChart and add the series to it
        self.chart = QChart()
        self.chart.addSeries(self.series)

        # Create a QValueAxis for the x axis, set its range, and add it to the chart
        self.x_axis = QValueAxis()
        self.x_axis.setRange(0, 10)  # Set the range of the x axis to 0-10
        self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        self.series.attachAxis(self.x_axis)

        # Create a QValueAxis for the y axis, set its range, and add it to the chart
        self.y_axis = QValueAxis()
        self.y_axis.setRange(-100, 100)  # Set the range of the y axis to 0-10
        self.chart.addAxis(self.y_axis, Qt.AlignLeft)
        self.series.attachAxis(self.y_axis)

        # Create a QChartView to display the chart
        self.chart_view = QChartView(self.chart)

        # Enable antialiasing for smoother lines
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Set the size policy of the QChartView to expanding
        self.chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab1_layout = QVBoxLayout()  # Define the layout
        self.tab1_layout.addWidget(self.chart_view)  # Add the chart view to the layout
        self.tab1_content.setLayout(self.tab1_layout)  # Set the layout for the tab content

        self.tab2_content = QWidget(self)
        self.tab2_layout = QVBoxLayout()  # Define the layout for the second tab

        # Add the labels and input fields
        self.question1_label = QLabel("Cколько вы сегодня поспали:", self)
        self.question1_input = QLineEdit(self)
        self.question2_label = QLabel("Меняли ли вы игровое место или посадку:", self)
        self.question2_input = QLineEdit(self)
        self.question3_label = QLabel("Какое у вас сегодня настроение:", self)
        self.question3_input = QLineEdit(self)

        # Add some styles to the labels and input fields
        self.question1_label.setStyleSheet("font: 16pt 'Arial'; color: #000000;")
        self.question1_input.setStyleSheet("""
                                                font: 14pt 'Arial';
                                                color: #000000;
                                                background-color: #87CEEB;
                                                border: none;
                                                border-radius: 15px;
                                                """)
        self.question2_label.setStyleSheet("font: 16pt 'Arial'; color: #000000;")
        self.question2_input.setStyleSheet("""
                                                font: 14pt 'Arial';
                                                color: #000000;
                                                background-color: #87CEEB;
                                                border: none;
                                                border-radius: 15px;
                                                """)
        self.question3_label.setStyleSheet("font: 16pt 'Arial'; color: #000000;")
        self.question3_input.setStyleSheet("""
                                                font: 14pt 'Arial';
                                                color: #000000;
                                                background-color: #87CEEB;
                                                border: none;
                                                border-radius: 15px;
                                                """)

        # Create the submit button
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setStyleSheet("""
            QPushButton {
                font: 16pt 'Arial';
                color: #FFFFFF;
                background-color: #87CEEB;
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #66B2FF;
            }
        """)

        # Add the labels and input fields to the layout
        self.tab2_layout.addWidget(self.question1_label)
        self.tab2_layout.addWidget(self.question1_input)
        self.tab2_layout.addWidget(self.question2_label)
        self.tab2_layout.addWidget(self.question2_input)
        self.tab2_layout.addWidget(self.question3_label)
        self.tab2_layout.addWidget(self.question3_input)

        # Add a stretch factor to push the submit button to the bottom
        self.tab2_layout.addStretch(1)

        # Add the submit button to the layout
        self.tab2_layout.addWidget(self.submit_button)

        self.tab2_content.setLayout(self.tab2_layout)  # Set the layout for the tab content

        # Add the second tab to the QTabWidget
        self.tab_widget.addTab(self.tab2_content, "Обратная связь")

        # Add the second tab to the QTabWidget

        # Create a QTextEdit for the third tab
        self.tab3_content = QTextEdit(self)
        self.tab3_content.setReadOnly(True)  # Make the QTextEdit read-only

        # Add the third tab to the QTabWidget
        self.tab_widget.addTab(self.tab3_content, "Настройки оверлея")
