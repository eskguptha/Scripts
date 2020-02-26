from abc import ABCMeta, abstractmethod
from utils.logger import glogger
import requests
import traceback
mport os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.conf import settings

import serial
import time
import traceback
from utils.logger import rs232logger
import datetime
from dc_abscomponent import DeviceCaptureABCComponent


class DeviceCaptureABCComponent():
    __metaclass__ = ABCMeta
    """
    Device Capture Component ABS Class
    """
    glogger.info("Invoke DeviceCaptureABCComponent")
    
    @abstractmethod
    def connect(self):
        """
        Connect to Device
        """
        pass
    @abstractmethod
    def disconnect(self):
        """
        Disconnect the connection
        """
        pass

    @abstractmethod
    def get_result(self):
        """
        Capture data packets from device
        """
        pass

    @abstractmethod
    def format_data(self):
        """
        Parse data packets
        """
        pass

    def post(self):
        """
        Post datapacket to API
        """
        glogger.info("POST API : Send API {} ".format(self.output_data['response']['api_payload']))
        try:
            if self.output_data['response']['api_payload']:
                print ("Send API POST Request to Dashboard")
            else:
                print ("No API Request Payload")
        except Exception:
            glogger.info("POST API : Exception: {} ".format(traceback.format_exc()))
        
        pass
class RS232DeviceResult(DeviceCaptureABCComponent):
    """RS232 Device Class for to capture the result from device"""
    def __init__(self, port):
        self.port = port
        self.baudrate = settings.RS232_BADRATE
        self.parity = settings.RS232_PARITY
        self.stopbits = settings.RS232_STOPBITS
        self.bytesize = settings.BYTESIZE
        self.logger =  rs232logger
        self.ser_con = None
        self.data_packet_recieve_counter = 0
        self.cmd_op_data_packets = ''
        self.response_max_wait_in_sec = 30
        self.cur_date_str = datetime.date.today().strftime("%m/%d/%Y")
        self.start_time = time.time()
        self.end_time = None
        self.output_data = {"response" : {"data" : '', "api_payload" : {}}, 'status' : False, "message" : ""}
        self.connect()
        self.get_result()
        self.disconnect()

    def connect(self):
        self.logger.info("connect : Create RS232 COM1 Connection")
        try:
            self.ser_con = serial.Serial(port=self.port,baudrate=self.baudrate,parity=self.parity,stopbits=self.stopbits,bytesize=self.bytesize)
        except Exception as e:
            self.logger.info("connect : Create RS232 COM1 Connection Exception. {}".format(traceback.format_exc()))
        pass
    def disconnect(self):
        self.logger.info("disconnect: Disconnect RS232 COM1 Connection")
        try:
            self.ser_con.close()
        except Exception as e:
            self.logger.info("disconnect: Disconnect RS232 COM1 Connection Exception. {}".format(traceback.format_exc()))
        pass
    
    def get_result(self):
        try:
            if self.ser_con.isOpen():
                self.logger.info("get_result : RS232 Connection Status : {}".format(self.ser_con.isOpen()))
                while 1 :
                    bytesToRead = self.ser_con.inWaiting()
                    cmd_res_str = self.ser_con.read(bytesToRead).strip()
                    cmd_res_str = cmd_res_str.replace('t', '').strip()
                    cmd_res_str = cmd_res_str.replace('', '').strip()
                    cmd_res_str = cmd_res_str.replace('(', '').strip()
                    cmd_res_str = cmd_res_str.replace(')', '').strip()
                    cmd_res_str = cmd_res_str.replace('\r', '').strip()
                    cmd_res_str = cmd_res_str.replace('.', '').strip()
                    cmd_res_str = cmd_res_str.replace(',', '').strip()
                   
                    self.logger.info("get_result: RS232 Device Connection DataPacket : {}".format(cmd_res_str))

                    # check date in datapacket
                    if self.cur_date_str in cmd_res_str:
                        self.output_data['response']['date'] = self.cur_date_str
                    
                    if cmd_res_str:
                        self.cmd_op_data_packets = self.cmd_op_data_packets + cmd_res_str
                        self.data_packet_recieve_counter = self.data_packet_recieve_counter +1

                    self.end_time = time.time()
                    self.elapsed_time = int(self.end_time - self.start_time)

                    if self.data_packet_recieve_counter >= 3 or self.elapsed_time > self.response_max_wait_in_sec:
                        self.output_data['status'] = True
                        self.format_data()
                        break    
                    time.sleep(1)
                    
            else:
                self.logger.info("get_result : RS232 Connection Status : {}".format(self.ser_con.isOpen()))
                self.output_data['status'] = False
        except AttributeError:
            self.logger.info("get_result : RS232 DataCapture Exception : {}".format(traceback.format_exc()))
            self.output_data['status'] = False
            self.output_data['message'] = "Connection Failed. Please check cable/port"  
        pass

    def format_data(self):
        self.logger.info("format_data : CMD Response before {}".format(self.cmd_op_data_packets))
        cmd_log = self.cmd_op_data_packets.split('\n')
        cmd_res = "<br/>".join(cmd_log)
        self.logger.info("format_data : CMD Response after {}".format(cmd_res))
        self.output_data['response']['data'] = cmd_res
        pass
if __name__ == '__main__':
    rs = RS232DeviceResult()
    rs.post()
    pass
