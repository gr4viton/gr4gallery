#!/usr/bin/python

# http://stackoverflow.com/questions/17073227/display-an-opencv-video-in-tkinter-using-multiprocessing
import array

import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
# import time
import Tkinter as tk
import Tkconstants, tkFileDialog

# from thisCV import *
# import numpy as np
# import cv2

import sys
import os
import glob

# tkinter GUI functions----------------------------------------------------------


class tkInterCV(tk.Frame):

    def __init__(q, root):
        print 'queue initialized...'
        q.imlLabel = q.GUI_setup(root)

        q.queue = Queue()
        q.root = root

        # q.HOTKEY_setup(root, p)



    def quit_(q, root, process, *whatever):
        process.terminate()
        root.destroy()


    # def quitCallback():

    def update_image(q, image_label, frame):
        if len(frame) == 0:
            return
        if len(frame.shape) == 2:
            im = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #im = frame


        a = Image.fromarray(im)
        b = ImageTk.PhotoImage(image=a)
        image_label.configure(image=b)
        image_label._image_cache = b  # avoid garbage collection
        q.root.update()

    def update_all(q, root, params):
        imlLabel, queue = params

        q.update_image(imlLabel, queue.get())
        root.after(0, func=lambda: q.update_all(root, params))

    def stepCV(q, cap):
        flag, frame = cap.read()
        if flag == 0:
            return None

        a = 0.5
        im = cv2.resize(frame, (0, 0), fx=a, fy=a)

        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return im

    # multiprocessing image processing functions-------------------------------------
    def image_capture(q, queue):
        cap = cv2.VideoCapture(0)
        loopingCV = 1
        while loopingCV:
            im = q.stepCV(cap)
            queue.put(im)
        cap.release()

    def SET_cwd(q):

        # os.getcwd()
        cwd = q.askdirectory()
        os.chdir(cwd)
        q.RECREATE_im()

    def RECREATE_im(q):
        print os.getcwd()
        pIms = glob.glob('*.png')
        print pIms
        # for pIm in pIms:
        #     imLabel.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
    def askdirectory(q):
        """Returns a selected directoryname."""

        # defining options for opening a directory
        dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        return tkFileDialog.askdirectory(**dir_opt)

    def GUI_setup(q, root):
        # GUI Items
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # frAddList
        # ____________________________________________________ frames
        frLeft = tk.LabelFrame(root, padx=5, width= 320, text="Add by list" )
        frTags = tk.LabelFrame(root, padx=5, width= 320, text="Detected tags")
        # ____________________________________________________ images
        imlLabel = tk.Label(frLeft)
        imlTags = tk.Label(frTags)
        # ____________________________________________________ texts
        # ____________________________________________________ sliders
        global slTags
        slTags = tk.Scale(frTags, from_=0, to_=10, orient=tk.HORIZONTAL)
        # ____________________________________________________ entries
        enHell = tk.Entry(frLeft, text='tkInter back in town')
        global strNumTags
        strNumTags = tk.StringVar()
        lbNumTags = tk.Label(frTags, textvariable=strNumTags)
        strNumTags.set( "0  found" )

        # ____________________________________________________ buttons
        btnQuit = tk.Button(frLeft, text='Q', command=lambda: q.quit_(root, p))
        # button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        button_opt = {'padx': 5, 'pady': 5}
        btnOpenFolder = tk.Button(frTags, text='askdirectory', command=q.SET_cwd)
        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # grid definitions
        #____________________________________________________
        frLeft.grid (row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

        imlLabel.grid(row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
        enHell.grid (row=1, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )
        btnQuit.grid(row=0, column=3, rowspan=4, columnspan=1, sticky=tk.NSEW )

        #____________________________________________________
        frTags.grid (row=2, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW )

        btnOpenFolder.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW, **button_opt)
        lbNumTags.grid(row=1, column=2, rowspan=1, columnspan=1)#, sticky=tk.NSEW )
        slTags.grid(row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW )


        print 'GUI initialized...'

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Key binding

        # return
        return imlLabel


    def HOTKEY_setup(q,root, p):
        # root.bind( '<Escape>', quit_(root, p) )
        pass

global instance
if __name__ == '__main__':
    root = tk.Tk()

    instance = tkInterCV(root)


    p = Process(target=instance.image_capture, args=(instance.queue,))

    p.start()
    print 'image capture process has started...'

    root.minsize(width=640, height=100)

    # setup the update callback (recursive calling inside)
    params = instance.imlLabel, instance.queue
    root.after(0, func=lambda: q.update_all(root, params))


    print 'root.after was called...'
    root.mainloop()
    print 'mainloop exit'
    p.terminate()
    # p.join()
    print 'image capture process exit'

    # answer
    # http://stackoverflow.com/questions/26834977/cannot-pickle-a-tkinter-object-in-a-multiprocessing-environment-in-windows