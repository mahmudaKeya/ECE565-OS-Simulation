import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, Toplevel, messagebox
import json
import sys
import os

#Additional_line
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from paths import *


print(PROJECT_ROOT)
#sys.path.append(PROJECT_ROOT)

# Explicitly add the Storage directory to the path

# Import your specific GUI classes
from  Storage.indexed.gui_indexed import IndexedAllocationBlockGUI,IndexedAllocationBLOCK
from Storage.contiguous.gui_contiguous import ContiguousAllocationBlockGUI
from Storage.linked.gui_linked import LinkedAllocationBlockGUI


from Storage.block import BLOCK, BlockGUI



# Run the main loop
def test_frame_request_to_storage():
    root = tk.Tk()
    #app = MainApp(root)
    '''
    Feel free to use any. It is the same address, anyway
    '''
    app=IndexedAllocationBlockGUI(root)
    return_frame=app.read(5)
    # app=ContiguousAllocationBlockGUI(root)
    # return_frame=app.read(5)
    # app=LinkedAllocationBlockGUI(root)
    # return_frame=app.read(5)
    print(return_frame)


    #root.mainloop()

test_frame_request_to_storage()