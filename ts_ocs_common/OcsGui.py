#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from OcsExceptions import *
from OcsLogger import *
import os
import sys
from ocs_id import *
from Tkinter import *
from tkMessageBox import *


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "15 January 2017"
__doc__ = """Common TkInter code for the OCS"""
__email__ = "pdaly@lsst.org"
__file__ = "OcsGui.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsQuitButton() inherits from Frame class
#-
class OcsQuitButton(Frame):

    #+
    # method: __init__
    #-
    def __init__(self, parent=None):
        if parent:
            Frame.__init__(self, parent)
            self.pack()
            widget = Button(self, text='Quit', command=self.quit)
            widget.config(foreground='black', background='wheat', font=('helvetica', 12, 'bold italic'))
            widget.pack(side=LEFT, expand=YES, fill=BOTH)

    #+
    # method: quit()
    #-
    def quit(self):
        if askokcancel('Verify Quit', 'Do you really want to quit this application?'):
            Frame.quit(self)


#+
# class: OcsDialog() inherits from Toplevel class
#-
class OcsDialog(Toplevel):

    #+
    # method: __init__
    #-
    def __init__(self, parent=None, title='', slist=[]):

        # get input(s)
        self.parent = parent
        self.slist = slist

        # initialize the superclass
        self.top = Toplevel.__init__(self, self.parent)
        self.transient(self.parent)
        self.title = title

        # create frame and buttons
        bd = Frame(self)
        bd.pack(padx=5, pady=5, expand=YES, fill=BOTH)
        self.initial_focus = self.body(bd,slist)
        self.createButtons()

        # do something
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.initial_focus.focus_set()
        self.focus_set()
        self.wait_window(self)

    #+
    # method: createButtons()
    #-
    def createButtons(self):

        # create buttons
        self.container = Frame(self)

        self.ok_button = Button(self.container, text='OK', width=10, command=self.ok, default=ACTIVE)
        self.ok_button.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        self.ok_button.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        self.ok_button.bind('<Return>', self.ok)
        self.ok_button.bind('<Button-1>', self.ok)
        self.ok_button.bind('<Button-3>', self.cancel)
        self.ok_button.bind('<Escape>', self.cancel)

        self.cancel_button = Button(self.container, text='Cancel', width=10, command=self.cancel)
        self.cancel_button.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        self.cancel_button.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        self.cancel_button.bind('<Return>', self.cancel)
        self.cancel_button.bind('<Button-1>', self.cancel)
        self.cancel_button.bind('<Button-3>', self.cancel)
        self.cancel_button.bind('<Escape>', self.cancel)

        self.container.pack()

    #+
    # method: ok()
    #-
    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.validate(True)
        self.parent.focus_set()
        self.destroy()

    #+
    # method: cancel()
    #-
    def cancel(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.validate(False)
        self.parent.focus_set()
        self.destroy()

    #+
    # (override) method: body()
    #-
    def body(self, parent=None, slist=[]):
        pass

    #+
    # (override) method: validate()
    #-
    def validate(self, okb=False):
        pass


#+
# class: OcsEntryDialog() inherits from the OcsDialog class
#-
class OcsEntryDialog(OcsDialog):

    # +
    # (overridden) method: body()
    # -
    def body(self, parent=None, slist=[]):
        self.slist = slist
        self.elist = []

        if not self.slist:
            return None

        for E in self.slist:
            idx = self.slist.index(E)
            Label(parent, text=E).grid(row=idx, column=0)
            iex = Entry(parent)
            iex.grid(row=idx, column=1)
            self.elist.append(iex)
        return self.elist[0]

    # +
    # (overridden) method: validate()
    # -
    def validate(self, okb=False):
        self.okb = okb

        if self.okb:
            self.parent.result = {}
            for k in self.slist:
                idx = self.slist.index(k)
                vp = self.elist[idx]
                if vp:
                    self.parent.result[k] = str(vp.get())
            return 0
        else:
            self.parent.result = {}
            return 1


# +
# main()
# -
if __name__ == '__main__':

    # get root frame
    root = Tk()

    # add parser
    parser = argparse.ArgumentParser()

    # add exclusive group
    group = parser.add_mutually_exclusive_group()

    # add exclusive argument(s)
    group.add_argument('-1', '--single', action="store_true", help="Test the single entry widget")
    group.add_argument('-2', '--double', action="store_true", help="Test the double entry widget")
    group.add_argument('-3', '--triple', action="store_true", help="Test the triple entry widget")
    group.add_argument('-4', '--quad', action="store_true", help="Test the quad entry widget")
    group.add_argument('-q', '--quit', action="store_true", help="Test the quit widget")

    # parse the command line arguments
    args = parser.parse_args()

    # test the single entry widget
    if args.single:
        OcsEntryDialog(root, 'Test Of Single Entry Widget', ['Input 1'])
        print("Returned dictionary = {0:s}".format(root.result))

    # test the double entry widget
    elif args.double:
        OcsEntryDialog(root, 'Test Of Double Entry Widget', ['Input 1', 'Input 2'])
        print("Returned dictionary = {0:s}".format(root.result))

    # test the trile entry widget
    elif args.triple:
        OcsEntryDialog(root, 'Test Of Triple Entry Widget', ['Input 1', 'Input 2', 'Input 3'])
        print("Returned dictionary = {0:s}".format(root.result))

    # test the quad entry widget
    elif args.quad:
        OcsEntryDialog(root, 'Test Of Quad Entry Widget', ['Input 1', 'Input 2', 'Input 3', 'Input 4'])
        print("Returned dictionary = {0:s}".format(root.result))

    # test the quit widget
    elif args.quit:
        OcsQuitButton(root).mainloop()

    # nothing specified on the command line
    else:
        print('No command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')

