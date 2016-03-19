#!/usr/bin/env python

##################
# pbm_viewer v2.0
##################
# ALDAPA taldea
# 2016 Otsaila
##################

import sys, math

import os

from Tkinter import * 
import tkMessageBox
from PIL import Image
import tkFileDialog
from ImageTk import PhotoImage              # <== required for JPEGs and others 

import datuak
from datuak import getPath
from thumbnails import wViewListImages

# Create the main object
images = datuak.pbmimages()

cluster_option=0

def selectclustering():
    global cluster_option
    cluster_option = v.get()
    
def selectpbmfile():
    # get filename
    filename = tkFileDialog.askopenfilename(filetypes=[("PBM file", ".pbm")])
    if filename:
#        label_filepbm.configure(text=filename)
        filenametail = os.path.split(filename)[1]
        label_filepbm.configure(text=filenametail)
        global images
        images = datuak.pbmimages()
        images.loadimgs(filename)
        btn_fileresults.configure(state=NORMAL)
        btn_viewimages.configure(state=NORMAL,text="View images (" + str(len(images.imgs)) + ")")

def selectresultsfile():
    # get filename
#     filename = tkFileDialog.askopenfilename(filetype=(("PBM",".pbm")))
    resultsfilename = tkFileDialog.askopenfilename(filetypes=[("arff file", ".arff"), ("CLA file", ".cla")])
    if resultsfilename:
        #label_fileresults.configure(text=resultsfilename)
        #tkMessageBox.showinfo("Info", "file:" + os.path.split(resultsfilename)[1])
        if os.path.splitext(resultsfilename)[1] == '.cla':
            err = images.loadresults(resultsfilename)
        elif os.path.splitext(resultsfilename)[1] == '.arff':
#            tkMessageBox.showinfo("Info", ".arrf file")
            err = images.loadresultsarff(resultsfilename,cluster_option)
        else:
            tkMessageBox.showwarning("Warning", "File type wrong!")
#            tkMessageBox.showerror("Error", "File type wrong!")
            return
        if err == -1:
            btn_viewresults.configure(state=DISABLED)
            return
        # Load correct
        resultsfilenametail = os.path.split(resultsfilename)[1]
        label_fileresults.configure(text=resultsfilenametail)
        if cluster_option==0: images.processResults()
        btn_viewresults.configure(state=NORMAL)

def ViewAll():
    listAll=[]
    for im in images.imgs:
        listAll.append((im.id,im.id))
    w = Toplevel()
    wView = wViewListImages(w,images,"View images",listAll)

def ViewAllClustering():
    listAll=[]
    for im in images.imgs:
        listAll.append((im.id,im.result))
    w = Toplevel()
    wView = wViewListImages(w,images,"View images",listAll)

def ViewList(idList):
    w = Toplevel()
    s = "View images: number %d - result %d" % (idList[0],idList[1])
    wView = wViewListImages(w,images,s,images.hits[idList[0]][idList[1]])

def processResults():
    images.processResults()
    images.showResultsTerminal()

def ViewTableResults():

    global cluster_option
    if cluster_option==1:
        ViewAllClustering()
        return

    w_results= Toplevel()
 
    Label(w_results, text = "Samples <--> results: mistakes", fg = '#006699', font = ('Papyrus', 18)).grid(row=0, column = 0, columnspan = 11)

    bigfra = LabelFrame(w_results,text="Samples <--> results",relief=GROOVE,borderwidth=2) 

    lerro   = 0
    zutabe  = 0

    Label(bigfra, text="Numbers").grid(row=lerro,column=zutabe)
    Label(bigfra, text="Mistaken with").grid(row=lerro,column=zutabe+1,columnspan=10)

    lerro+=1

    Label(bigfra, text=" ").grid(row=lerro,column=zutabe)
    for i in range(10):
        zutabe += 1 
        Label(bigfra, text=i).grid(row=lerro,column=zutabe)

    for ro in range(10):
        lerro+=1
        zutabe=0
        Label(bigfra, text=ro).grid(row=lerro,column=zutabe)
        for co in range(10):
            zutabe += 1 
            if ro==co and 1==0:
                Label(bigfra, text="X").grid(row=lerro,column=zutabe)
            else:
                if (len(images.hits[ro][co])==0):
                    Label(bigfra, text="-").grid(row=lerro,column=zutabe)
                else:
                    link = Button(bigfra, text=str(len(images.hits[ro][co])))
                    link.grid(row=lerro,column=zutabe)
                    handler = lambda r=[ro,co]: ViewList(r)  
                    link.config(command=handler)
    bigfra.grid()


# create root window
w_root = Tk()
# creates an instance / object of class Tk
w_root.title("pbm_viewer v2.0")
# displays a nice title on the window
Label(w_root, text = "pbm viewer", fg = '#006699', font = ('Papyrus', 18)).grid(row=0, column = 0, columnspan = 11)

btn_viewimages = Button(w_root, text='View images', command=ViewAll, state=DISABLED,wraplength='4c',width='15')
btn_viewimages.grid(row=1,column=0,sticky=NW)
btn_filepbm = Button(w_root, text='Select a pbm file', command=selectpbmfile,wraplength='4c',width='15')
btn_filepbm.grid(row=1,column=1,sticky=NW)
label_filepbm = Label(w_root, text = "No file",width=40,anchor=W)
label_filepbm.grid(row=1, column = 2)

btn_viewresults = Button(w_root, text='View results', command=ViewTableResults, state=DISABLED,wraplength='4c',width='15')
btn_viewresults.grid(row=2,column=0,sticky=NW)
btn_fileresults = Button(w_root, text='Select a results file', command=selectresultsfile, state=DISABLED,wraplength='4c',width='15')
btn_fileresults.grid(row=2,column=1,sticky=NW)
label_fileresults = Label(w_root, text = "No file",width=40,anchor=W)
label_fileresults.grid(row=2, column = 2)

v=IntVar()
Checkbutton(w_root, text='Clustering', state=NORMAL, anchor=W, command=selectclustering, variable=v).grid(row=3, column=1, sticky=W)

btn_exit = Button(w_root, text='Exit', command=w_root.destroy, width='8')
btn_exit.grid(row=3,column=2,sticky=SE)

# start event-loop
# keeps displaying the window until we kill it.
w_root.mainloop()
# images.loadimgs("a.pbm")
# ViewAll()


if __name__ == '__main__': 
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or 'images' 
#     main, save = viewer(images,images.mistakes, kind=Tk) 
#     main.mainloop( ) 


