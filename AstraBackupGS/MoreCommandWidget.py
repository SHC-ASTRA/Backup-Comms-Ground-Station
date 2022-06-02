from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MoreCommandWidget(QWidget):
    command_sent = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        layout = QGridLayout()
        self.setLayout(layout)

        # pid_button = QPushButton("Update PID")
        fin_button = QPushButton("Set Antenna Heading")
        fin_button_1 = QPushButton("Set Base Lon")
        fin_button_2 = QPushButton("Set Base Lat")
        # state_button = QPushButton("Set State")
        custom_button = QPushButton("Custom Command")

        # kp_box = QLineEdit()
        # kp_box.setPlaceholderText("Kp")
        # kp_box.setValidator(QDoubleValidator())
        # ki_box = QLineEdit()
        # ki_box.setPlaceholderText("Ki")
        # ki_box.setValidator(QDoubleValidator())
        # kd_box = QLineEdit()
        # kd_box.setPlaceholderText("Kd")
        # kd_box.setValidator(QDoubleValidator())

        # pid_button.clicked.connect(lambda clicked:
        #                            self.send_command(f"PID/{float(kp_box.text()) if kp_box.text() != '' else 0.0 :05.2f}/{float(ki_box.text()) if ki_box.text() != '' else 0.0 :05.2f}/{float(kd_box.text()) if kd_box.text() != '' else 0.0 :05.2f}\n"))

        fin_box = QLineEdit()
        fin_box.setPlaceholderText("Heading")
        fin_box.setValidator(QDoubleValidator())

        fin_button.clicked.connect(lambda clicked:
                                   self.send_command(f"MANUAL_HEADING;{float(fin_box.text()) if fin_box.text() != '' else 0.0 :05.1f}\n"))

        fin_box_1 = QLineEdit()
        fin_box_1.setPlaceholderText("Base Longitude")
        fin_box_1.setValidator(QDoubleValidator())

        fin_button_1.clicked.connect(lambda clicked:
                                   self.send_command(f"MANUAL_GPS_BASE_LON;{float(fin_box.text()) if fin_box.text() != '' else 0.0 :05.1f}\n"))

        fin_box_2 = QLineEdit()
        fin_box_2.setPlaceholderText("Base Latitude")
        fin_box_2.setValidator(QDoubleValidator())

        fin_button_2.clicked.connect(lambda clicked:
                                   self.send_command(f"MANUAL_GPS_BASE_LAT;{float(fin_box.text()) if fin_box.text() != '' else 0.0 :05.1f}\n"))

        # state_box = QLineEdit()
        # state_box.setPlaceholderText("State #")
        # state_box.setValidator(QIntValidator())

        # state_button.clicked.connect(lambda clicked:
        #                              self.send_command(f"STATE/{int(state_box.text()) if state_box.text() != '' else 0 :02}\n"))

        custom_box = QLineEdit()
        custom_box.setPlaceholderText("Command")

        custom_button.clicked.connect(lambda clicked:
                                     self.send_command(custom_box.text() + "\n"))

        # layout.addWidget(pid_button, 0, 0)
        # layout.addWidget(kp_box, 0, 1)
        # layout.addWidget(ki_box, 0, 2)
        # layout.addWidget(kd_box, 0, 3)

        layout.addWidget(fin_button, 1, 0)
        layout.addWidget(fin_box, 1, 1, 1, 3)

        layout.addWidget(fin_button_2, 3, 0)
        layout.addWidget(fin_box_2, 3, 1, 1, 3)
        layout.addWidget(fin_button_1, 4, 0)
        layout.addWidget(fin_box_1, 4, 1, 1, 3)

        # layout.addWidget(state_button, 2, 0)
        # layout.addWidget(state_box, 2, 1, 1, 3)

        layout.addWidget(custom_button, 2, 0)
        layout.addWidget(custom_box, 2, 1, 1, 3)


    def send_command(self, command):
        print(command)
        self.command_sent.emit(command)
