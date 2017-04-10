#!/usr/bin/env python
# -*- coding: utf-8 -*-


# +
# import(s)
# -
from ocs_id import *
# noinspection PyCompatibility,PyCompatibility
from Tkinter import *
# noinspection PyCompatibility
from tkMessageBox import *

import logging

# +
# __doc__ string
# -
__doc__ = """

This file, $TS_OCS_COMMON_SRC/OcsGui.py, contains code for common operations within a TkInter OCS GUI.
Note that this code is temporary as these interfaces will be replaced by web-based interfaces in due course,
It uses argparse to provide a command line interface. There are no Python (unit) tests.

Import:

    from OcsGui import *

Example:

    evh = None
    try:
        root = Tk()
        evh = OcsEntryDialog(root, 'Test', ['Input Line 1'])
    except:
        pass

API:

    OcsEntryDialog(OcsDialog)
        this class provides support for a pop-up window with a variable number of input lines and a pair of operation
        buttons (Ok, Cancel). If 'Ok' is selected, a dictionary of values can be returned to higher level code.

    OcsQuitButton(Frame)
        this class contains the single method 'quit' which produces a Quit button with a verification dialog widget

    OcsTextHandler(logging.Handler)
        this class provides support for sending logger outputs to a text handler within the main GUI frame. See an
        example in $TS_OCS_SEQUENCER_SRC/OcsGenericSequencerGui.py
    
CLI:

    [pnd@localhost ts_ocs_common]$ python OcsGui.py --help
    usage: OcsGui.py [-h] [-1 | -2 | -3 | -4 | -q]

    optional arguments:
      -h, --help    show this help message and exit
      -1, --single  Test the single entry widget
      -2, --double  Test the double entry widget
      -3, --triple  Test the triple entry widget
      -4, --quad    Test the quad entry widget
      -q, --quit    Test the quit widget

"""


# +
# dunder string(s)
# -
__author__ = "Philip N. Daly"
__copyright__ = u"\N{COPYRIGHT SIGN} AURA/LSST 2017. All rights reserved. Released under the GPL."
__date__ = "15 January 2017"
__email__ = "pdaly@lsst.org"
__file__ = "OcsGui.py"
__history__ = __date__ + ": " + "original version (" + __email__ + ")"
__version__ = "0.1.0"


# +
# class: OcsTextHandler() inherits from logging.Handler
# -
class OcsTextHandler(logging.Handler):

    # +
    # method: __init__
    # -
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    # +
    # method: emit()
    # -
    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(END)
        # necessary because we can't modify the Text from other threads
        self.text.after(0, append)


# +
# class: OcsQuitButton() inherits from Frame class
# -
class OcsQuitButton(Frame):

    # +
    # method: __init__
    # -
    def __init__(self, parent=None):
        if parent:
            Frame.__init__(self, parent)
            self.pack()
            widget = Button(self, text='Quit', command=self.quit)
            widget.config(foreground='black', background='wheat', font=('helvetica', 12, 'bold italic'))
            widget.pack(side=LEFT, expand=YES, fill=BOTH)

    # +
    # method: quit()
    # -
    def quit(self):
        if askokcancel('Verify Quit', 'Do you really want to quit this application?'):
            Frame.quit(self)


# +
# class: OcsDialog() inherits from Toplevel class
# -
class OcsDialog(Toplevel):

    # +
    # method: __init__
    # -
    def __init__(self, parent=None, title='', slist=None):

        # get input(s)
        self.parent = parent
        self.slist = list(slist)
        self.elist = None

        # declare some variables and initialize them
        self._event = None

        # initialize the superclass
        self.top = Toplevel.__init__(self, self.parent)
        self.transient(self.parent)
        self.title = title

        # create frame and buttons
        bd = Frame(self)
        bd.pack(padx=5, pady=5, expand=YES, fill=BOTH)
        self.initial_focus = self.body(bd, self.slist)
        self.create_buttons()

        # do something
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.initial_focus.focus_set()
        self.focus_set()
        self.wait_window(self)

    # +
    # method: createButtons()
    # -
    def create_buttons(self):

        # create buttons
        container = Frame(self)

        ok_button = Button(container, text='OK', width=10, command=self.ok, default=ACTIVE)
        ok_button.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        ok_button.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        ok_button.bind('<Return>', self.ok)
        ok_button.bind('<Button-1>', self.ok)
        ok_button.bind('<Button-3>', self.cancel)
        ok_button.bind('<Escape>', self.cancel)

        cancel_button = Button(container, text='Cancel', width=10, command=self.cancel)
        cancel_button.pack(side=LEFT, padx=5, pady=5, expand=YES, fill=BOTH)
        cancel_button.config(foreground='black', background='wheat', font=('helvetica', 10, 'bold italic'))
        cancel_button.bind('<Return>', self.cancel)
        cancel_button.bind('<Button-1>', self.cancel)
        cancel_button.bind('<Button-3>', self.cancel)
        cancel_button.bind('<Escape>', self.cancel)

        container.pack()

    # +
    # method: ok()
    # -
    def ok(self, event=None):
        self._event = event
        self.withdraw()
        self.update_idletasks()
        self.validate(True)
        self.parent.focus_set()
        self.destroy()

    # +
    # method: cancel()
    # -
    def cancel(self, event=None):
        self._event = event
        self.withdraw()
        self.update_idletasks()
        self.validate(False)
        self.parent.focus_set()
        self.destroy()

    # +
    # (override) method: body()
    # -
    def body(self, parent=None, slist=None):
        pass

    # +
    # (override) method: validate()
    # -
    def validate(self, okb=False):
        pass


# +
# class: OcsEntryDialog() inherits from the OcsDialog class
# -
class OcsEntryDialog(OcsDialog):

    # +
    # (overridden) method: body()
    # -
    def body(self, parent=None, slist=None):
        self.slist = list(slist)
        self.elist = []

        if not self.slist:
            return None

        for El in self.slist:
            idx = self.slist.index(El)
            Label(parent, text=El).grid(row=idx, column=0)
            iex = Entry(parent)
            iex.grid(row=idx, column=1)
            self.elist.append(iex)
        return self.elist[0]

    # +
    # (overridden) method: validate()
    # -
    def validate(self, okb=False):

        if okb:
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
