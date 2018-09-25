#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.13
# In conjunction with Tcl version 8.6
#    Aug 09, 2018 11:51:25 AM

import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import BDE_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    BDE_support.set_Tk_var()
    top = BDE_v0_1 (root)
    BDE_support.init(root, top)
    root.mainloop()

w = None
def create_BDE_v0_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    BDE_support.set_Tk_var()
    top = BDE_v0_1 (w)
    BDE_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_BDE_v0_1():
    global w
    w.destroy()
    w = None


class BDE_v0_1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {Segoe UI} -size 20 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font9 = "-family {Segoe UI} -size 14 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("480x256+462+226")
        top.title("BDE v0.1")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.cmdKommen = Button(top)
        self.cmdKommen.place(relx=0.15, rely=0.39, height=64, width=137)
        self.cmdKommen.configure(activebackground="#d9d9d9")
        self.cmdKommen.configure(activeforeground="#000000")
        self.cmdKommen.configure(background="#d9d9d9")
        self.cmdKommen.configure(disabledforeground="#a3a3a3")
        self.cmdKommen.configure(font=font9)
        self.cmdKommen.configure(foreground="#000000")
        self.cmdKommen.configure(highlightbackground="#d9d9d9")
        self.cmdKommen.configure(highlightcolor="black")
        self.cmdKommen.configure(pady="0")
        self.cmdKommen.configure(text='''Kommen''')
        self.cmdKommen.bind('<Button-1>',lambda e:BDE_support.Buchung("kommen"))

        self.cmdGehen = Button(top)
        self.cmdGehen.place(relx=0.58, rely=0.39, height=64, width=137)
        self.cmdGehen.configure(activebackground="#d9d9d9")
        self.cmdGehen.configure(activeforeground="#000000")
        self.cmdGehen.configure(background="#d9d9d9")
        self.cmdGehen.configure(disabledforeground="#a3a3a3")
        self.cmdGehen.configure(font=font9)
        self.cmdGehen.configure(foreground="#000000")
        self.cmdGehen.configure(highlightbackground="#d9d9d9")
        self.cmdGehen.configure(highlightcolor="black")
        self.cmdGehen.configure(pady="0")
        self.cmdGehen.configure(text='''Gehen''')
        self.cmdGehen.bind('<Button-1>',lambda e:BDE_support.Buchung("gehen"))

        self.lblAP = Label(top)
        self.lblAP.place(relx=0.02, rely=0.12, height=51, width=464)
        self.lblAP.configure(activebackground="#f9f9f9")
        self.lblAP.configure(activeforeground="black")
        self.lblAP.configure(background="#d9d9d9")
        self.lblAP.configure(disabledforeground="#a3a3a3")
        self.lblAP.configure(font=font10)
        self.lblAP.configure(foreground="#000000")
        self.lblAP.configure(highlightbackground="#d9d9d9")
        self.lblAP.configure(highlightcolor="black")
        self.lblAP.configure(text='''Station: ???''')
        self.lblAP.configure(width=464)

        self.lblOutput = Label(top)
        self.lblOutput.place(relx=0.19, rely=0.78, height=21, width=284)
        self.lblOutput.configure(activebackground="#f9f9f9")
        self.lblOutput.configure(activeforeground="black")
        self.lblOutput.configure(background="#d9d9d9")
        self.lblOutput.configure(disabledforeground="#a3a3a3")
        self.lblOutput.configure(foreground="#000000")
        self.lblOutput.configure(highlightbackground="#d9d9d9")
        self.lblOutput.configure(highlightcolor="black")
        self.lblOutput.configure(text='''Label''')

        self.menubar = Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=BDE_support.Login_AP,
                font="TkMenuFont",
                foreground="#000000",
                label="Login")
        self.menubar.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=BDE_support.exitButton,
                font="TkMenuFont",
                foreground="#000000",
                label="Exit")


        self.lblVersion = Label(top)
        self.lblVersion.place(relx=0.0, rely=0.86, height=21, width=35)
        self.lblVersion.configure(activebackground="#f9f9f9")
        self.lblVersion.configure(activeforeground="black")
        self.lblVersion.configure(background="#d9d9d9")
        self.lblVersion.configure(disabledforeground="#a3a3a3")
        self.lblVersion.configure(foreground="#000000")
        self.lblVersion.configure(highlightbackground="#d9d9d9")
        self.lblVersion.configure(highlightcolor="black")
        self.lblVersion.configure(text='''vx.x''')

        self.lblTest = Label(top)
        self.lblTest.place(relx=0.81, rely=0.86, height=21, width=64)
        self.lblTest.configure(activebackground="#f9f9f9")
        self.lblTest.configure(activeforeground="black")
        self.lblTest.configure(background="#d9d9d9")
        self.lblTest.configure(disabledforeground="#a3a3a3")
        self.lblTest.configure(foreground="#000000")
        self.lblTest.configure(highlightbackground="#d9d9d9")
        self.lblTest.configure(highlightcolor="black")
        self.lblTest.configure(text='''Label''')
        self.lblTest.configure(textvariable=BDE_support.lblTest_var)
        self.lblTest.configure(width=64)






if __name__ == '__main__':
    vp_start_gui()



