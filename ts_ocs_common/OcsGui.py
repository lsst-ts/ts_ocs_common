#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# Python 2.x -> 3.x compatability function(s)
# -
from __future__ import print_function


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
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2016. All rights reserved. Released under the GPL."
__date__ = "31 October 2016"
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

        # set up logging
        self.logger = OcsLogger('OCS', 'Gui').logger
        self.logger.debug("Starting {0:s}".format(self.title))

        # create frame and buttons
        bd = Frame(self)
        bd.pack(padx=5, pady=5, expand=YES, fill=BOTH)
        self.initial_focus = self.body(bd,slist)
        self.createButtons()

        # do something
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.initial_focus.focus_set()
        self.focus_set()
        self.wait_window(self)

    #+
    # method: createButtons()
    #-
    def createButtons(self):

        # create buttons
        box = Frame(self)
        w = Button(box, text='OK', width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        w.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        w = Button(box, text='Cancel', width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        w.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        box.pack()

    #+
    # method: ok()
    #-
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.validate()
        self.cancel()

    #+
    # method: cancel()
    #-
    def cancel(self, event=None):
        self.parent.result = {}
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
    def validate(self):
        pass

    #+
    # (override) method: apply()
    #-
    def apply(self):
        pass


#+
# class: OcsEntryDialog() inherits from the OcsDialog class
#-
class OcsEntryDialog(OcsDialog):

    # +
    # (overridden) method: body()
    # -
    def body(self, parent=None, slist=[]):
        self.elist = []
        self.slist = slist
        if self.slist:
            for E in self.slist:
                idx = self.slist.index(E)
                Label(parent, text=E).grid(row=idx, column=0)
                iex = Entry(parent)
                iex.grid(row=idx, column=1)
                self.elist.append(iex)
            return self.elist[0]
        else:
            return None

    # +
    # (overridden) method: validate()
    # -
    def validate(self):
        self.parent.result = {}
        if self.slist:
            for E in self.slist:
                idx = self.slist.index(E)
                self.parent.result[str(E)] = self.elist[idx].get()
            self.logger.debug("Returning {0:s}".format(str(self.parent.result)))
            return 1
        else:
            return 0

    # +
    # (overridden) method: apply()
    # -
    def apply(self):
        self.validate()


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
    group.add_argument('-f', '--setfilter', action="store_true", help="Test the setFilter widget")
    group.add_argument('-g', '--initguiders', action="store_true", help="Test the initGuiders widget")
    group.add_argument('-i', '--initimage', action="store_true", help="Test the initImage widget")
    group.add_argument('-p', '--setvalue', action="store_true", help="Test the setValue widget")
    group.add_argument('-q', '--quit', action="store_true", help="Test the quit widget")
    group.add_argument('-s', '--start', action="store_true", help="Test the start widget")
    group.add_argument('-t', '--takeimages', action="store_true", help="Test the takeImages widget")
    group.add_argument('-x', '--stop', action="store_true", help="Test the stop widget")

    # parse the command line arguments
    args = parser.parse_args()

    # test the parameter-value widget
    if args.setvalue:
        OcsEntryDialog(root, 'setValue()', ['Parameter', 'Value'])

    # test the start widget
    elif args.start:
        OcsEntryDialog(root, 'start()', ['StartId'])

    # test the stop widget
    elif args.stop:
        OcsEntryDialog(root, 'stop()', ['Device'])

    # test the quit widget
    elif args.quit:
        OcsQuitButton(root).mainloop()

    # test the initguiders widget
    elif args.initguiders:
        OcsEntryDialog(root, 'initGuider()', ['roiSpec'])

    # test the initimage widget
    elif args.initimage:
        OcsEntryDialog(root, 'initImage()', ['deltaT'])

    # test the setfilter widget
    elif args.setfilter:
        OcsEntryDialog(root, 'setFilter()', ['name'])

    # test the takeimages widget
    elif args.takeimages:
        OcsEntryDialog(root, 'takeImages()', ['numImages', 'expTime', 'shutter', 'science', 'guide', 'wfs', 'imageSequenceName'])

    # nothing specified on the command line
    else:
        print('No command line arguments specified')
        print('Use: python ' + sys.argv[0] + ' --help for more information')

