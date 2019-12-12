from tkinter import Tk, CallWrapper
from gui import GUI
from config import logger


if __name__ == '__main__':

    def report_callback_exception(self, exc, val, tb):
        logger.exception(('/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\\'))

    Tk.report_callback_exception = report_callback_exception

    root = Tk()
    gui = GUI(root)
    root.mainloop()