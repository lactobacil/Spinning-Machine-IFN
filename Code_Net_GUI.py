# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 12:09:50 2021


GUI TKINTER AND 
@author: Wikara
"""

#Netting Counter Data Transfer
import minimalmodbus
import os
import sys
import mysql.connector
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import*
import datetime
from time import sleep
import schedule
 
#The packages has to be open to 
sys.path.append('/home/pi/.local/lib/python3.7/site-packages/mysql')
#Connecting To mysql apache server computer
 
#assign portname, slave address (in decimal), check with ls /dev/tty*
instrument = minimalmodbus.Instrument('/dev/ttyUSB0',1)
#instrument properties
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.stopbits = 1
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU
instrument.clear_buffers_before_each_transaction = True
instrument.debug = True
#instrument setting ends here
 
 
 
class MainWindow:
    def __init__(self, master):
        #master properties of Tkinter
        master.geometry("700x300")
        master.resizable(0,0)
        master.title("Netting Machine No. 185 Instruksi Pengerjaan")
        #Initialise Variables Boolean or Ints
        self.RpmBool     = False
        self.QuitBoolean = False
 
 
        #MySQL Initiator, Connect To database, setting goes here
        """
 
        self.conn = mysql.connector.connect(host="10.10.7.27",
                                       user="root",
                                       passwd="",
                                       database="counter")
 
        self.c = conn.cursor()
        """
 
        #Input Maximum Digit When Send Data
        self.DigInput = Entry(master, width=15)
        self.DigInput.pack()
        self.DigInput.place(x=50, y=40)
 
        #Input Name When Send to Database
        self.NameInput = Entry(master, width=15)
        self.NameInput.pack()
        self.NameInput.place(x=50, y=120)
 
        #Record Maximum RPM
        self.CmdInput = tk.Button(master, text = "Input Maximum RPM", command=self.RpmMax)
        self.CmdInput.pack()
        self.CmdInput.place(x=50, y=80)
 
        self.NameLabel = tk.Button(master, text = "Input Name", command=self.GetName)
        self.NameLabel.pack()
        self.NameLabel.place(x=50, y=140)
        #Quit Button Goes here
        self.NameLabel = tk.Button(master, text = "Quit", command=self.QuitBool)
        self.NameLabel.pack()
        self.NameLabel.place(x=400, y=40)
 
 
        #Status Digit currently goes here, update will continue 
        self.status = Label(master, text = "RPM Count")
        self.status.config(font=('Helvetica bold', 80))
        self.status.pack(side='right')
 
        #RPMData goes here with the details: time, name and maximum current
        self.RPMdata = Label(master, text = "Maximum RPM")
        self.RPMdata.config(font=('Helvetica bold', 20))
        self.RPMdata.pack(side='bottom')
 
        #RPMName Goes Here
        self.RPMname = Label(master, text = "Username:")
        self.RPMname.config(font=('Helvetica bold', 20))
        self.RPMname.pack(side='bottom')
 
    def create_table():
        self.c.execute('CREATE TABLE IF NOT EXISTS counts (instr REAL, datestamp TEXT, keyword TEXT, value REAL, ip TEXT, name TEXT)')
        self.conn.commit()
 
    def shiftime(self):
        self.instr = "RPM Spinning"
        #Obtain Datetime here, when RPMMax reached datetime is collected
        self.date = date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
 
        print(self.date)
 
        #self.c.execute("""UPDATE counts SET instr=%s, datestamp=%s, keyword=%s, value= %s""",
        #      (self.instr, self.date, self.keyword, self.value))
        #self.conn.commit()
 
 
    def TestPrint(self):
        print('Testyay+++++++++++++++++++++++++++++++++++++++++++++++++++++')
 
    def DigiUpdate(self, digit_count):
        self.status["text"] = digit_count
 
    def RpmMax(self):
        self.RpmBool = True
        self.rpm_ip = int(self.DigInput.get())
        self.RPMdata["text"] = "RPM Finish:" + self.DigInput.get()
 
    def GetName(self):
        self.Username = self.NameInput.get()
        self.RPMname["text"] = "Username:" + self.Username
        #Here Goes Main Function iteration, this acts like main
 
    def QuitBool(self):
        self.QuitBoolean = True
 
    def ReadDigit(self):
        schedule.run_pending()
        #Read long digit from 1003 (Register), (4 is mode), True (Signed/Unsigned), BYTEORDER = 0
        self.digit_count = instrument.read_registers(1003,1,4)
        self.status["text"] = self.digit_count
        self.rpmdat = self.digit_count[0]
 
        #Scheduler Goes Here, for timelogs
        schedule.every().day.at("18:43").do(self.TestPrint)
        schedule.every().day.at("20:00").do(self.TestPrint)
 
        #Insert Name, Values if RPM Passed and if rpmdat has passed the target
        if self.RpmBool == True:
            if self.rpmdat == self.rpm_ip:
                print("RPMSent")
 
                #Send data to Database if finished
                #self.c.execute("INSERT INTO counts (ip, name) VALUES ('%s', '%s');"
                #  %(self., self.digit_count))
                #self.conn.commit()
 
        #How many time will it acquisite data goes here
        root.after(1000, self.ReadDigit)
 
        #def SQLSend(self):
 
 
root = Tk()
NetCount = MainWindow(root)
 
schedule.every().day.at("18:57").do(NetCount.TestPrint)
schedule.every().day.at("20:00").do(NetCount.TestPrint)
 
while NetCount.QuitBoolean == False:
    schedule.run_pending()
    root.after(2, NetCount.ReadDigit)
    root.mainloop()
 