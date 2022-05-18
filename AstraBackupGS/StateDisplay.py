from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class StateDisplay(QWidget):

    def __init__(self, mode_key, met_key, jetson_packet_key):
        super().__init__()

        self.mode_key = mode_key
        self.met_key = met_key
        self.jetson_packet_key = jetson_packet_key

        self.init_ui()

    def init_ui(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.mode_box = QLineEdit()
        self.mode_box.setReadOnly(True)
        f = QFont()
        f.setBold(True)
        f.setPointSize(24)
        self.mode_box.setFont(f)
        self.mode_box.setAlignment(Qt.AlignCenter)
        self.mode_box.setMinimumSize(160, 0)

        self.met_box = QLCDNumber()
        self.met_box.setDigitCount(10)
        self.met_box.display("00000000")
        self.jetson_packet_box = QLCDNumber()
        self.jetson_packet_box.setDigitCount(10)
        self.jetson_packet_box.display("00000000")

        layout.addWidget(QLabel(self.mode_key), 0, 0)
        layout.addWidget(QLabel(self.met_key), 1, 0)
        layout.addWidget(QLabel(self.jetson_packet_key), 2, 0)

        layout.addWidget(self.mode_box, 0, 1)
        layout.addWidget(self.met_box, 1, 1)
        layout.addWidget(self.jetson_packet_box, 2, 1)

    def update_state(self, dictionary):
        self.mode_box.setText(dictionary[self.mode_key])
        self.met_box.display(dictionary[self.met_key])
        self.jetson_packet_box.display(dictionary[self.jetson_packet_key])


        # met_time = int(dictionary[self.met_key])
        # met_seconds = str(int(met_time % 60)).zfill(2)
        # met_minutes = str(int((int(met_time/60)) % 60)).zfill(2)
        # met_hours = str(int((met_time/60)/60)).zfill(2)
        # self.met_box.display(met_hours+":"+met_minutes+":"+met_seconds)

        # jet_time = int(dictionary[self.jetson_packet_key])
        # jet_seconds = str(int(jet_time % 60)).zfill(2)
        # jet_minutes = str(int((int(jet_time/60)) % 60)).zfill(2)
        # jet_hours = str(int((jet_time/60)/60)).zfill(2)
        # self.jet_box.display(jet_hours+":"+jet_minutes+":"+jet_seconds)