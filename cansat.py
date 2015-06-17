__author__ = 'prempal'

import serial
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
FILE_NAME = "CANSAT2015_TLM_<TEAM_ID>.csv"
HEADER_ROW = ['TEAM_ID','MISSION_TIME','ALT_SENSOR','OUTSIDE_TEMP','INSIDE_TEMP',
'VOLTAGE','FSW_STATE','BONUS']

fig = plt.figure()
fig.canvas.set_window_title('REALTIME DATA PLOTTING')

ser = serial.Serial(SERIAL_PORT,BAUD_RATE)
myFile = open(FILE_NAME,'wb')
writer = csv.writer(myFile)
writer.writerow(HEADER_ROW)
i = 0
xar = []
out_temp, in_temp, altitude, acc_x, acc_y, acc_z = [], [], [], [], [], []
def animate(yolo):
    global i, xar, out_temp, in_temp, altitude, acc_x, acc_y, acc_z
    message = ser.readline()
    if len(message)>5:
        l = message.split(",")
        print l
        #remove the newline character from the end
        l = l[:-1]
        xyz = l[7:]
        l = l[:7]
        l.append(xyz)
        writer.writerow(l)
        xar.append(int(i))
        altitude.append(float(l[2]))
        out_temp.append(float(l[3]))
        in_temp.append(float(l[4]))
        x = int(xyz[0])
        y = int(xyz[0])
        z = int(xyz[0])
        acc_x.append(x)
        acc_y.append(y)
        acc_z.append(z)
        descent_angle = math.acos(math.sqrt(x*x + y*y + z*z)/math.sqrt(x*x + y*y))
        print descent_angle
        i = i+1

    plt.subplot(3, 2, 1)
    plt.plot(xar,out_temp,'yo-')
    plt.xlabel('Time(s)')
    plt.ylabel('Outside Temperature(deg C)')

    plt.subplot(3, 2, 2)
    plt.plot(xar,in_temp,'ro-')
    plt.xlabel('Time(s)')
    plt.ylabel('Inside Temperature(deg C)')

    plt.subplot(3, 2, 3)
    plt.plot(xar,altitude,'go-')
    plt.xlabel('Time(s)')
    plt.ylabel('Altitude(m)')

    plt.subplot(3, 2, 4)
    plt.plot(xar,acc_x,'bo-')
    plt.plot(xar,acc_y,'go-')
    plt.plot(xar,acc_z,'yo-')
    plt.xlabel('Time(s)')
    plt.ylabel('Acceleration(m/s^2)')

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()