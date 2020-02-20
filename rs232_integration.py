'''
pySerial’s
This module encapsulates the access for the serial port. It provides backends for Python
running on Windows, OSX, Linux, BSD (possibly any POSIX compliant system) and IronPython.
The module named “serial” automatically selects the appropriate backend.
pyserial==3.4
'''

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'lcgcseedsqtkit.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.conf import settings

import serial
import time
import traceback
import logging
import datetime

import serial
RS232_PORT = "COM1"
RS232_BADRATE = 9600
RS232_PARITY = serial.PARITY_ODD
RS232_STOPBITS = serial.STOPBITS_TWO
BYTESIZE = serial.SEVENBITS


class RS232DeviceResult():
    """RS232 Device Class for to capture the result from device"""
    def __init__(self):
        self.port = RS232_PORT
        self.baudrate = RS232_BADRATE
        self.parity = RS232_PARITY
        self.stopbits = RS232_STOPBITS
        self.bytesize = BYTESIZE
        self.logger =  logging.getLogger('rs232')
        self.ser_con = None
        self.data_packet_recieve_counter = 0
        self.cur_date_str = datetime.date.today().strftime("%m/%d/%Y")
        self.output_data = {"response" : {"data" : ''}, 'status' : False, "message" : ""}
        self.get_result()

    def connect(self):
        self.logger.info("Create RS232 COM1 Connection")
        try:
            self.ser_con = serial.Serial(port=self.port,baudrate=self.baudrate,parity=self.parity,stopbits=self.stopbits,bytesize=self.bytesize)
        except Exception as e:
            self.logger.info("Create RS232 COM1 Connection Exception. {}".format(traceback.format_exc()))
            self.logger.info("{}".format(traceback.format_exc()))
        pass
    def disconnect(self):
        self.logger.info("Disconnect RS232 COM1 Connection")
        try:
            self.ser_con.close()
        except Exception as e:
            self.logger.info("Disconnect RS232 COM1 Connection Exception. {}".format(traceback.format_exc()))
            self.logger.info("{}".format(traceback.format_exc()))
        pass
    def format_data(self):
        self.logger.info("format_data : CMD Response before {}".format(self.cmd_op_data_packets))
        cmd_log = self.cmd_op_data_packets.split('\n')
        cmd_res = "<br/>".join(cmd_log)
        self.logger.info("format_data : CMD Response after {}".format(cmd_res))
        self.output_data['response']['data'] = cmd_res
        pass
        
    def get_result(self):
        self.connect()
        self.cmd_op_data_packets = ''
        self.start_time = time.time()
        try:
            if self.ser_con.isOpen():
                self.logger.info("RS232 Connection Status : {}".format(self.ser_con.isOpen()))
                while 1 :
                    bytesToRead = self.ser_con.inWaiting()
                    cmd_res_str = self.ser_con.read(bytesToRead).strip()
                    cmd_res_str = cmd_res_str.replace('t', '').strip()
                    cmd_res_str = cmd_res_str.replace('', '').strip()
                    cmd_res_str = cmd_res_str.replace('(', '').strip()
                    cmd_res_str = cmd_res_str.replace('\r', '').strip()
                    cmd_res_str = cmd_res_str.replace('.', '').strip()
                    cmd_res_str = cmd_res_str.replace(',', '').strip()
                   
                    self.logger.info("RS232 Device Connection DataPacket : {}".format(cmd_res_str))

                    # check date in datapacket
                    if self.cur_date_str in cmd_res_str:
                        self.output_data['response']['date'] = self.cur_date_str
                    
                    if cmd_res_str:
                        self.cmd_op_data_packets = self.cmd_op_data_packets + cmd_res_str
                        self.data_packet_recieve_counter = self.data_packet_recieve_counter +1

                    self.end_time = time.time()
                    self.elapsed_time = int(self.end_time - self.start_time)

                    if self.data_packet_recieve_counter >= 3 or self.elapsed_time > 30:
                        self.output_data['status'] = True
                        self.format_data()
                        break    
                    time.sleep(1)
                    
            else:
                self.logger.info("RS232 Connection Status : {}".format(self.ser_con.isOpen()))
                self.output_data['status'] = False
        except AttributeError:
            self.logger.info("RS232 DataCapture Exception : {}".format(traceback.format_exc()))
            self.output_data['status'] = False
            self.output_data['message'] = "Connection Failed. Please check cable/port"  

        self.disconnect()
        pass
