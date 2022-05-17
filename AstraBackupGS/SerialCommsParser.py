from PyQt5.QtCore import *

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class SerialCommsParser(QObject):

    parsed = pyqtSignal(dict)
    gps_parsed = pyqtSignal(dict)
    packet_info_parsed = pyqtSignal(dict)
    packet_data_parsed = pyqtSignal(dict)
    packet = pyqtSignal(str)
    command = pyqtSignal(str)
    message = pyqtSignal(str)
    error = pyqtSignal(str)
    warning = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.topic_map = {
            "data_packet": self.packet_data_parsed,
            "gps": self.gps_parsed,
            "packet_info": self.packet_info_parsed
        }

    def parse(self, text):

        if text.startswith("CMD TX:"):
            self.command.emit(text)
            return

        if "unexpected" in text or "Too many retries" in text or "failed" in text:
            self.error.emit(text)
            return

        args = text.split(";")
        topic = args[0]
        data = args[1]

        if topic == "status":
            self.message.emit(data)
        else:
            try:
                pairs = data.split(',')
                results = {}
                for pair in pairs:
                    name, value = pair.split('=')
                    results[name] = value

                self.topic_map[topic].emit(results)
            
            except:
                print(text, "Parse failure\n")

        self.packet.emit(text)
