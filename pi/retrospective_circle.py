"""

@authors: brennamanning, jovanduy, redfern314

Reads accelerometer data from csv file
Creates animated plot of recorded data on a circular graph

TO RUN: python retrospective_circle.py (CSV FILE NAME)
ex:
TO RUN: python retrospective_circle.py 2014-01-19_14:56:32.csv

"""

import csv,sys
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ACCEL_CONVERSION = 4096

colors = ["r","b","g","c","m","k"]
labels = ["pitch","roll","yaw","accelX","accelY","accelZ","latitude","longitude","altitude","GPS_fix"]

def read_file(filename):
    """ Read the .csv made from collecting data from the arduIMU.
        filename: path to the .csv
        returns: dictionary of the different data columns of the arduIMU
    """
    rawData = {}
    for i in range(6):
        rawData[labels[i]] = []

    with open(filename, 'rb') as csvfile:
        IMUreader = csv.reader(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # read all the data
        for row in IMUreader:
            if row[0] != "pitch": # first row is headers
                rawData["pitch"].append(float(row[0]))
                rawData["roll"].append(float(row[1]))
                rawData["yaw"].append(float(row[2]))
                rawData["accelX"].append(float(row[3]))
                rawData["accelY"].append(float(row[4]))
                rawData["accelZ"].append(float(row[5]))

    return rawData

def create_circle_graph():
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    circle = plt.Circle((0,0), radius=2, color='r', fill=False)
    plt.plot([-.0001,.0001],[-2,2],'k-')
    plt.plot([-2,2],[-.0001,.0001],'k-')
    ax.set_xlim((-2,2))
    ax.set_ylim((-2,2))
    ax.add_patch(circle)
    return fig, ax, circle

def update_circle_graph(fig, ax, circle, x, y):
    fig.clf()
    fig.gca().add_artist(circle)
    plt.plot([-.0001,.0001],[-2,2],'k-')
    plt.plot([-2,2],[-.0001,.0001],'k-')
    plt.plot(x, y, marker='o', color='blue', linestyle='None')
    ax.set_xlim((-2,2))
    ax.set_ylim((-2,2))
    plt.pause(.01)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        rawData = read_file(sys.argv[1])
        fig, ax, circle = create_circle_graph()
        for i in range(len(rawData["accelX"])):
            update_circle_graph(fig, ax, circle, rawData["accelX"][i]/ACCEL_CONVERSION, rawData["accelY"][i]/ACCEL_CONVERSION)
        # plt.legend()
        plt.show()

    else:
        print "Please specify a .csv"