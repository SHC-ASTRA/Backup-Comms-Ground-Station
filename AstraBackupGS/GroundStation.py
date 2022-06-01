import sys

from PyQt5.QtWidgets import *

import CommandWidget
import CommsLog
import CommsParser
import GSGraph
import SerialComms as sc
import SerialCommsParser
import FileComms as fc
import StateDisplay
import dark_fusion
from MoreCommandWidget import MoreCommandWidget
from QTabWidgetResize import QTabWidgetResize
import roslibpy


huntsville = False


class Screen(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASTRA Backup Comms Station")

        self.comm_w = sc.SerialConnectionWidget()
        self.file_w = fc.FileConnectionWidget()
        self.parser = SerialCommsParser.SerialCommsParser()

        self.comm_w.received.connect(self.parser.parse)
        self.file_w.received.connect(self.parser.parse)
        self.log_w = CommsLog.CommsLog()
        self.cmds = CommandWidget.CommandWidget({"Halt": "HALT;",
                                                 "Enable Jetson": "ENABLE;",
                                                 "Set Freq 905": "SET_FREQ;905",
                                                 "Set Freq 915": "SET_FREQ;915",
                                                 "Set Freq 925": "SET_FREQ;925",
                                                 "Enable Tracking": "TRACKING_ENABLE;",
                                                 "Disable Tracking": "TRACKING_DISABLE;",
                                                 "Enable Pointing": "POINTING_ENABLE",
                                                 "Disable Pointing": "POINTING_DISABLE"})

        self.more_cmds = MoreCommandWidget()

        self.state_disp = StateDisplay.StateDisplay("mode", "elapsed_time", "last_jetson_packet_time")
        self.parser.packet_data_parsed.connect(self.state_disp.update_state)

        self.gps_disp = StateDisplay.StateDisplay("gps_time", "gs_latitude", "gs_longitude")
        self.parser.gps_parsed.connect(self.gps_disp.update_state)

        self.rover_gps_disp = StateDisplay.StateDisplay("command_ack", "rover_latitude", "rover_longitude")
        self.parser.packet_data_parsed.connect(self.rover_gps_disp.update_state)

        self.antenna_tracking_disp = StateDisplay.StateDisplay("active_tracking", "target_heading", "heading")
        self.parser.compass_parsed.connect(self.antenna_tracking_disp.update_state)

        self.voltage_plot = GSGraph.GSGraph("elapsed_time", "battery_voltage",
                                            title="Battery Voltage", x_units="Milliseconds", y_units="Volts")
        self.parser.packet_data_parsed.connect(self.voltage_plot.update_plot)
        self.left_rpm_plot = GSGraph.GSGraph("elapsed_time", "left_wheels_rpm",
                                            title="Left Wheels RPM", x_units="Milliseconds", y_units="RPM")
        self.parser.packet_data_parsed.connect(self.left_rpm_plot.update_plot)
        self.right_rpm_plot = GSGraph.GSGraph("elapsed_time", "right_wheels_rpm",
                                            title="Right Wheels RPM", x_units="Milliseconds", y_units="RPM")
        self.parser.packet_data_parsed.connect(self.right_rpm_plot.update_plot)

        self.rssi_plot = GSGraph.GSGraph("gs_time", "rssi",
                                            title="RSSI", x_units="Milliseconds", y_units="")
        self.parser.packet_info_parsed.connect(self.rssi_plot.update_plot)
        self.snr_plot = GSGraph.GSGraph("gs_time", "snr",
                                            title="SNR", x_units="Milliseconds", y_units="")
        self.parser.packet_info_parsed.connect(self.snr_plot.update_plot)

        if not huntsville:
            lat_min = 32.2345
            lat_max = 32.2545
            lon_min = -98.2120
            lon_max = -98.1883
            image_name = "CroppedMap.png"

        else:
            lat_min = 34.7145
            lat_max = 34.736
            lon_min = -86.6525
            lon_max = -86.6266
            image_name = "HuntsvilleCropped.png"

        self.parser.packet.connect(self.log_w.log_packet)
        self.parser.message.connect(self.log_w.log_message)
        self.parser.command.connect(self.log_w.log_command)
        self.parser.error.connect(self.log_w.log_error)
        self.parser.warning.connect(self.log_w.log_warning)

        self.cmds.command_sent.connect(self.comm_w.transmit)
        self.more_cmds.command_sent.connect(self.comm_w.transmit)

        layout = QVBoxLayout()
        self.setLayout(layout)

        primary_graph_holder = QWidget()
        primary_graph_layout = QGridLayout(primary_graph_holder)
        primary_graph_layout.addWidget(self.state_disp, 0, 0)
        primary_graph_layout.addWidget(self.gps_disp, 0, 1)
        primary_graph_layout.addWidget(self.rover_gps_disp, 0, 2)
        primary_graph_layout.addWidget(self.antenna_tracking_disp, 0, 3)

        primary_graph_layout.addWidget(self.voltage_plot, 1, 0)
        primary_graph_layout.addWidget(self.left_rpm_plot, 1, 1)
        primary_graph_layout.addWidget(self.right_rpm_plot, 1, 2)
        primary_graph_layout.addWidget(self.rssi_plot, 1, 3)
        primary_graph_layout.addWidget(self.snr_plot, 1, 4)

        top_tabwidget = QTabWidgetResize()
        top_tabwidget.addTab(primary_graph_holder, "Primary Display")

        clear_all_btn = QPushButton("Clear All Graphs")
        clear_all_btn.setParent(top_tabwidget)
        top_tabwidget.resized.connect(lambda event: clear_all_btn.move(event.size().width()-clear_all_btn.width(), 0))
        clear_all_btn.show()
        clear_all_btn.clicked.connect(self.voltage_plot.clear_plot)
        clear_all_btn.clicked.connect(self.left_rpm_plot.clear_plot)
        clear_all_btn.clicked.connect(self.right_rpm_plot.clear_plot)
        clear_all_btn.clicked.connect(self.snr_plot.clear_plot)
        clear_all_btn.clicked.connect(self.rssi_plot.clear_plot)

        botton_tabwidget = QTabWidget()
        botton_tabwidget.setMinimumWidth(450)
        botton_tabwidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        botton_tabwidget.addTab(self.comm_w, "Connection Settings")
        botton_tabwidget.addTab(self.file_w, "File Reader")
        botton_tabwidget.addTab(self.cmds, "Commands 1")
        botton_tabwidget.addTab(self.more_cmds, "Commands 2")

        bottom_layout_holder = QWidget()
        bottom_layout = QHBoxLayout(bottom_layout_holder)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.log_w)
        bottom_layout.addWidget(botton_tabwidget)

        layout.addWidget(top_tabwidget)
        layout.addWidget(bottom_layout_holder)

        self.ros = roslibpy.Ros(host="192.168.1.2", port=9090)
        self.ros.run()

        self.gps_subscriber = roslibpy.Topic(self.ros, "/teensy/gps_native", "sensor_msgs/NavSatFix")
        def command_manual_gps_target(gps_fix):
            self.comm_w.transmit(f"MANUAL_GPS_TARGET_LAT;{gps_fix['latitude']}\n")
            self.comm_w.transmit(f"MANUAL_GPS_TARGET_LON;{gps_fix['longitude']}\n")
        self.gps_subscriber.subscribe(command_manual_gps_target)


def run():
    app = QApplication(sys.argv)
    dark_fusion.set_style(app)
    w = Screen()
    w.show()
    app.exec_()


run()
