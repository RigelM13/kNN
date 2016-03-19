#!/usr/bin/env python

import sys, math

from Tkinter import * 
from datuak import getPath
import Image, ImageTk


gmaxItems=100
gmaxColumns=10

gmaxItems=50
gmaxColumns=10

xbmBlank="""
#define a2_width 27
#define a2_height 32
static char a2_bits[] = {
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00};
"""

# from PIL import Image
class ClassThumbnail:
    def __init__(self,id,path,num,data):

        self.id=StringVar()
        self.id.set(id)

#         self.path=StringVar()
#         self.path.set(path)

        self.number=StringVar()
        self.number.set(num)

        self.data=StringVar()
        self.data.set(data)

class wViewListImages:

    def __init__(self,parent,imagesCollection, sCaption, listId):
        self.master = parent    # store parent window

        self.imagesCollection= imagesCollection

        if sCaption=="View images":
            import operator
            listId=sorted (listId,key=operator.itemgetter(1))
            self.listId = map(operator.itemgetter(0),listId)    # store id of imgs to view
        else:
            self.listId = listId    # store id of imgs to view

        self.pagethumbsCaption  = StringVar()
        self.pagethumbs = [] # store data of imgs in the current page
        self.photothumbs = [] # store data of imgs in the current page
        self.photolabels = [] # store data of imgs in the current page

        self.maxItems=gmaxItems
        self.maxColumns=gmaxColumns 
        
        self.fraMain = Frame(parent)     # frame to group all widgets

        Label(self.fraMain, text = sCaption, fg = '#006699', font = ('Papyrus', 20)).grid(row=0, column = 0, columnspan = 11)

        fraControl = Frame(self.fraMain)     # frame to group all widgets

        LabelCaption= Label(fraControl , textvariable = self.pagethumbsCaption, fg = '#0000ff', font = (12))
        LabelCaption.pack(side=TOP)

        fraControlButtons = Frame(fraControl)     # frame to group all widgets
        fraControlButtons.pack(side=TOP)

        self.btnPrevious = Button(fraControlButtons, text='Previous', command=self.GoPreviousPage, width='8')
#         btnPrevious.grid(row=1,column=1,sticky=SE)
        self.btnPrevious.pack(side=LEFT, fill=Y)

        self.btnNext = Button(fraControlButtons, text='Next', command=self.GoNextPage, width='8')
#         btnNext.grid(row=1,column=2,sticky=SE)
        self.btnNext.pack(side=RIGHT, fill=Y)

        fraControlListBox = Frame(fraControl)     # frame to group all widgets
        fraControlListBox.pack(side=TOP)
        self.listbox = Listbox(fraControlListBox)
        self.listbox.bind('<Double-Button- 1>',self.ListBoxChangePage)
#         listbox.grid(row=2,column=1,columnspan=2)
        listboxscrollbar = Scrollbar(fraControlListBox)
#         listboxscrollbar.grid()

        self.listbox.pack(side=LEFT, fill=Y)
        listboxscrollbar.pack(side=RIGHT, fill=Y)

        listboxscrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=listboxscrollbar.set)

        btn_exit = Button(fraControl, text='Exit', command=self.master.destroy, width='8')
#         btn_exit.grid(row=2,column=0,sticky=SE)
        btn_exit.pack(side=TOP)

        numPages= len(self.listId) / self.maxItems
        if len(self.listId) % self.maxItems > 0:
            numPages+=1
#         print numPages

        for page in range(numPages):
            if page < (numPages-1):
                s = "from %s to %s" % (str(page*self.maxItems),str(page*self.maxItems+self.maxItems-1))
            else:
                s = "from %s to %s" % (str(page*self.maxItems),str(len(self.listId)-1))
            self.listbox.insert(END, s)

        fraControl.grid(row=1,column=0,sticky=N)

        #############

        fraImages = Frame(self.fraMain)     # frame to group all widgets

#         LabelCaption= Label(fraImages, textvariable = self.pagethumbsCaption, fg = '#006699', font = ('Papyrus', 20))
#         LabelCaption.grid(row=0, column = 0, columnspan = 11)

#         self.pictures=[]

        rownum = 1
        colnum = 1

        for i in range(self.maxItems):

            thumb = ClassThumbnail(str(i),"blank.gif","","")
            self.pagethumbs.append(thumb)

            fra = Frame(fraImages,relief=RIDGE,borderwidth=1,padx=2,pady=2)

            Label(fra, textvariable=self.pagethumbs[i].id).grid(row=1,column=1,columnspan=2)
#             imgThumb = ImageTk.PhotoImage(file='blank.gif')
            imgThumb = ImageTk.BitmapImage(data=xbmBlank)
            LabelImg = Label(fra, image=imgThumb ,width='60')
            LabelImg.grid(row=2,column=1,rowspan=3)
            self.photothumbs.append(imgThumb)
            self.photolabels.append(LabelImg)
            Label(fra, textvariable=self.pagethumbs[i].number).grid(row=2,column=2)
            
            Label(fra, textvariable=self.pagethumbs[i].data).grid(row=4,column=2)

            fra.grid(row=rownum,column=colnum,sticky= N)
            colnum += 1
            if colnum > self.maxColumns:
                rownum += 1
                colnum = 1

        fraImages.grid(row=1,column=1)

        self.page=0
        self.LoadPage(0)

        self.fraMain.grid()

    def LoadPage(self, numpage):

        numPages= len(self.listId) / self.maxItems
        if len(self.listId) % self.maxItems > 0:
            numPages+=1
        if numpage <0 or numpage > numPages:
            print "Error: number of page (%d) not correct",numpage
            # Error
        self.page=numpage

        indexFrom   = numpage*self.maxItems
        indexTo     = (numpage+1)*self.maxItems
        if indexTo > len(self.listId):
            indexTo=len(self.listId)
        s = "From %s to %s" % (indexFrom,indexTo-1)

        self.pagethumbsCaption.set(s)

        if numpage==0:
            self.btnPrevious.config(state=DISABLED)
        else:
            self.btnPrevious.config(state=ACTIVE)

        if numpage==numPages-1 or numPages==0:
            self.btnNext.config(state=DISABLED)
        else:
            self.btnNext.config(state=ACTIVE)

        self.listbox.selection_clear(0,self.listbox.size()-1)
        self.listbox.see(numpage)
        self.listbox.selection_set(numpage)

        indexthumb=0
        for indeximg in range(indexFrom,indexTo):

            imgId = self.listId[indeximg]

            objimg = self.imagesCollection.imgs[imgId]
#             objimg.saveImagepbm()

            self.pagethumbs[indexthumb].id.set(imgId)
            self.pagethumbs[indexthumb].number.set(objimg.number)
            if objimg.result!=-1:
                self.pagethumbs[indexthumb].data.set(objimg.result)
            else:
                self.pagethumbs[indexthumb].data.set(" ")

            self.photothumbs[indexthumb]= ImageTk.BitmapImage(data=objimg.textxbm)
            self.photolabels[indexthumb].configure(image=self.photothumbs[indexthumb])
            indexthumb+=1

        while (indexthumb<self.maxItems):
#             print indexthumb
            self.pagethumbs[indexthumb].id.set("-")
            self.pagethumbs[indexthumb].number.set("-")
            self.pagethumbs[indexthumb].data.set("-")
            self.photothumbs[indexthumb]= ImageTk.BitmapImage(data=xbmBlank)
            self.photolabels[indexthumb].configure(image=self.photothumbs[indexthumb])
            indexthumb+=1

#         for i in range(indexthumb,self.maxItems):
#             self.pagethumbs[i].id.set("-")

#         print len(self.pagethumbs)

    def GoNextPage(self):
        self.LoadPage(self.page+1)

    def GoPreviousPage(self):
        self.LoadPage(self.page-1)

    def ListBoxChangePage(self,event):
        selected=self.listbox.curselection()
        if len(selected)==1:
#             print(selected[0])
         self.LoadPage(int(selected[0]))
    

# list = []
# for i in range(213):
#     list.append(i)
# # create root window
# root=Tk()
# wView = wViewListImages(root,"View images",list)
# root.mainloop()
