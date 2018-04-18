from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from  tkinter import filedialog ,ttk
import os
import matplotlib
import hashlib
import sqlite3
import json
matplotlib.use("TkAgg")
import tkinter as tk
from PIL import Image
savedate = []
count = []
def json2port(json):
    listLatLon = []

    if len(json['Data']) > 0:
        listLatLon.append(((float(json["Data"][0]["Latitude"])),(float(json["Data"][0]["Longitude"]))))
        for i in range(len(json["Data"])):
            for j in range(len(listLatLon)):
                if listLatLon[j] == ((float(json["Data"][i]["Latitude"])),(float(json["Data"][i]["Longitude"]))):
                    #listLatLon.append((float(json["Data"][i]["Latitude"]),(float(json["Data"][i]["Longitude"]))))
                    break
                else:
                    if j == (len(listLatLon)-1):
                        listLatLon.append((float(json["Data"][i]["Latitude"]),float(json["Data"][i]["Longitude"])))
    print(listLatLon)
    plotchart(json,listLatLon)

def plotmap(json,LatLon):
    plt.figure(figsize=(5,5))
    from mpl_toolkits.basemap import Basemap
    i = 0
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
       llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    m.drawparallels(np.arange(-90.,91.,30.))
    m.drawmeridians(np.arange(-180.,181.,60.))
    m.drawmapboundary(fill_color='aqua')
    plt.savefig("map.png")
    for i in range(len(LatLon)):
        lat = float(LatLon[i][0])
        lon = float(LatLon[i][1])
        x,y = m(lon, lat)
        m.plot(x, y, 'bo', markersize=5)
        plt.savefig("mapplot.png")
        background = Image.open("map.png")
        overlay = Image.open("mapplot.png")
        new_img = Image.blend(background, overlay,0.5)
        print("hello")
        new_img.save("new.png","PNG")
    fsttime.append("ok")
    a.show()



def plotchart(json,listLatLon):
    plt.figure(figsize=(5,5))
    labels = []
    sizes = []
    for i in range(len(json["topten"])):
        if (len(json["topten"]) == len(labels)) or (len(labels) == 10):
            break
        else:
            labels.append(json["topten"][i][0])
            sizes.append(json["topten"][i][1])

    patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("piechart.png")
    plt.clf()
    plotmap(json,listLatLon)

filename = []
fsttime = []
dateFirst = []
dateLast = []
Month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,
             "Jul":7, "Aug":8, "Sep":9, "Oct":10,"Nov":11,
             "Dec":12}
def re_date():

    if len(filename) > 0:
        log_file = open(filename[len(filename) - 1], "r")
        text = log_file.read()
        date = (re.findall(r'\[(?P<date>[^\[\]:]+):(?P<time>\d+:\d+:\d+) (?P<tz>[\-\+]?\d\d\d\d)\]',text))
        DateMonthFirst = date[0][0].split("/")
        print(DateMonthFirst)
        print(DateMonthFirst[0])
        dateFirst.append((DateMonthFirst[0],Month[DateMonthFirst[1]],DateMonthFirst[2]))
        DateMonthLast = date[len(date)-1][0].split("/")
        print(DateMonthLast)

        dateLast.append((DateMonthLast[0],Month[DateMonthLast[1]],DateMonthLast[2]))
        print("!!!!!!!!!!")
        print(dateLast)
        print("!!!!!!!!!!")
        print((dateLast))
        log_file.close()

def setday1():
    #print(dateFirst)
   #return int(dateFirst[0][len(dateFirst[0])-2])-1
   return (int(dateFirst[0][len(dateFirst[0])-3])-1)
def setday2():
   return (int(dateLast[0][len(dateLast[0])-3])-1)
def setmonth1():
    #return int(dateFirst[0][len(dateFirst[0])-1])-1
    #return int(Month[dateLast[0][len(dateLast[0])-2]])-1
    return (int(dateFirst[0][len(dateFirst[0])-2])-1)
def setmonth2():
    return (int(dateLast[0][len(dateLast[0])-2])-1)
def setyear1():
     return int(dateFirst[0][len(dateFirst[0])-1])-2000
def setyear2():
    return int(dateLast[0][len(dateLast[0])-1])-2000

class Gui:
    def __init__(self):
        self.day = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        self.month = [1,2,3,4,5,6,7,8,9,10,11,12]
        self.year = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
        self.root = tk.Tk()
        self.root.geometry("1200x720") #screen resolution
        self.root.title('App')


    def day_first(self):
        print("5555")
        print(filename)

        self.browsefile = tk.Button(self.root, text="Browse", command = self.browse_file)
        self.browsefile.grid(column=1, row=1, sticky="ne")


        self.okbutton = tk.Button(self.root, text="OK", command = self.sendday)
        self.okbutton.grid(column=10, row=1, sticky="ne")

        self.text_first = tk.Label(self.root, text=" First")
        self.text_first.grid(column=2, row=1, sticky="nesw")
        self.text_second = tk.Label(self.root, text=" Second")
        self.text_second.grid(column=6, row=1, sticky="nesw")

        self.d1 = ttk.Combobox(self.root)
        self.d1.grid(column=3, row=1, sticky="ne")
        self.d1['value'] = self.day
        if len(fsttime) == 0:
            self.d1.current(0)
        elif len(fsttime) == 1:
            self.d1.current(setday1())
        else:
            self.d1.current(savedate[0][len(savedate[0])-6])


        self.m1 = ttk.Combobox(self.root)
        self.m1.grid(column= 4, row= 1, sticky="ne")
        self.m1['value'] = self.month
        if len(fsttime) == 0:
            self.m1.current(0)
        elif len(fsttime) == 1:
            self.m1.current(setmonth1())
        else:
            self.m1.current(savedate[0][len(savedate[0])-5])

        self.y1 = ttk.Combobox(self.root)
        self.y1.grid(column= 5, row= 1, sticky="ne")
        self.y1['value'] = self.year

        if len(fsttime) == 0:
            self.y1.current(0)
        elif len(fsttime) == 1:
            self.y1.current(setyear1())
        else:
            self.y1.current(savedate[0][len(savedate[0])-4])

    # def day_second(self):

        self.d2 = ttk.Combobox(self.root)
        self.d2.grid(column= 7, row=1, sticky="ne")
        self.d2['value'] = self.day
        if len(fsttime) == 0:
            self.d2.current(0)
        elif len(fsttime) == 1:
            self.d2.current(setday2())
        else:
            self.d2.current(savedate[0][len(savedate[0])-3])

        self.m2 = ttk.Combobox(self.root)
        self.m2.grid(column= 8, row= 1, sticky="ne")
        self.m2['value'] = self.month
        if len(fsttime) == 0:
            self.m2.current(0)
        elif len(fsttime) == 1:
            self.m2.current(setmonth2())
        else:
            self.m2.current(savedate[0][len(savedate[0])-2])
        self.y2 = ttk.Combobox(self.root)
        self.y2.grid(column= 9, row= 1, sticky="ne")
        self.y2['value'] = self.year
        if len(fsttime) == 0:
            self.y2.current(0)
        elif len(fsttime) == 1:
            self.y2.current(setyear2())
        else:
            self.y2.current(savedate[0][len(savedate[0])-1])

        # self.okbutton = tk.Button(self.root, text="OK", command = self.sendday)
        # self.okbutton.grid(column=10, row=1, sticky="ne")
        print("kkkkkkkkkkkk")
        savedate.clear()
        self.root.mainloop()

    def browse_file(self):
        print(dateFirst)
        print(dateLast)
        print(savedate)
        currdir = os.getcwd()
        name = filedialog.askopenfilename(initialdir=currdir, title='Please select a file')
        filename.append(name)
        if len(filename) > 0:
            try:
                dateFirst.clear()
                dateLast.clear()
                re_date()
                savedate.clear()
                savedate.append((int(dateFirst[0][len(dateFirst[0])-3])-1,int(dateFirst[0][len(dateFirst[0])-2])-1,int(dateFirst[0][len(dateFirst[0])-1])-2000,
                                    int(dateLast[0][len(dateLast[0])-3])-1,int(dateLast[0][len(dateLast[0])-2])-1,int(dateLast[0][len(dateLast[0])-1])-2000))

                fsttime.clear()
                fsttime.append("1")
                f = open(filename[len(filename) - 1], "rb")
                file = f.read()
                con = sqlite3.connect('C:/Users/Bankjaa/work1_ip.db')
                c = con.cursor()
                for j in c.execute('SELECT Max(md5) FROM data_md5'):
                    pass
                for i in c.execute('SELECT * FROM data_md5'):
                    if i[0] == hashlib.md5(file).hexdigest():
                        name = hashlib.md5(file).hexdigest()
                        filejson = open("{}{}".format(name,".json"), "r")
                        datajson = json.load(filejson)
                        json2port(datajson)
                        fsttime.append("2")
                        print("aaaaaaaaaaaaaaaaaaaaaaa")
                        print(dateFirst)
                        print(dateLast)
                        print(fsttime)
                        print(savedate)
                        self.day_first()
                        break
                    else:
                        if i[0] == j[0]:
                            fsttime.clear()
                            self.show()
                            fsttime.append("1")
                            self.day_first()


            except:
                print("666666666666666")
                pass



    def sendday(self):
        print("1412")
        if len(filename) > 0:

            if len(fsttime) == 0:
                savedate.clear()
                re_date()
                savedate.append((int(dateFirst[0][len(dateFirst[0])-3])-1,int(dateFirst[0][len(dateFirst[0])-2])-1,int(dateFirst[0][len(dateFirst[0])-1])-2000,
                                     int(dateLast[0][len(dateLast[0])-3])-1,int(dateLast[0][len(dateLast[0])-2])-1,int(dateLast[0][len(dateLast[0])-1])-2000))
            else:
                savedate.clear()
                savedate.append((int(self.d1.get())-1,int(self.m1.get())-1,int(self.y1.get())-2000,int(self.d2.get())-1,int(self.m2.get())-1,int(self.y2.get())-2000))
            import access2json
            acess = access2json.accesslog2json(self.d1.get(),self.m1.get(),self.y1.get(),
                                               self.d2.get(),self.m2.get(),self.y2.get(),filename)
            acess.openFile()

            f = open(filename[len(filename) - 1], "rb")
            file = f.read()
            f.close()

            name = hashlib.md5(file).hexdigest()
            try:
                filejson = open("{}{}".format(name,".json"), "r")
                datajson = json.load(filejson)
                fsttime.clear()
                fsttime.append("1")
                fsttime.append("2")
                json2port(datajson)
            except:
                if len(fsttime) == 0:
                    fsttime.clear()
                    self.show()

                else:
                    fsttime.clear()
                    self.show()
                    fsttime.append("1")

            self.day_first()



    def show(self):
        if len(fsttime) == 0:
            try:
                self.img1 = PhotoImage(file = "map.png")
                self.imgmap = Label(self.root, image = self.img1)
                self.imgmap.grid(column=1, row=2, columnspan = 5)

                img2 = PhotoImage(file = "piechart.png")
                imgmap = Label(self.root, image = img2)
                imgmap.grid(column=6, row=2, columnspan = 5)
            except:
                pass
        else:
            try:
                self.img1 = PhotoImage(file = "mapplot.png")
                self.imgmap = Label(self.root, image = self.img1)
                self.imgmap.grid(column=1, row=2, columnspan = 5)

                self.img2 = PhotoImage(file = "piechart.png")
                self.imgmap = Label(self.root, image = self.img2)
                self.imgmap.grid(column=7, row=2, columnspan = 5)
            except:
                pass



a = Gui()
a.show()
a.day_first()
