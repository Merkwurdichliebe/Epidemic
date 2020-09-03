import tkinter as tk
from tkinter import ttk
from webbrowser import open as webopen


def display_help(root):
    def cb_open_web():
        webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')
        popup.destroy()

    popup = tk.Toplevel()
    popup.title('Epidemic Help')
    text = 'Help is available on the application\'s GitHub page.'
    lbl1 = tk.Label(popup, text=text, pady=10, padx=20)
    lbl1.pack()

    frm_btns = tk.Frame(popup, pady=10)
    frm_btns.pack()

    btn = tk.Button(frm_btns, text='View in browser', width=15, command=cb_open_web)
    btn.pack(side=tk.LEFT, padx=5)
    btn = tk.Button(frm_btns, text='Close', width=15, command=popup.destroy)
    btn.pack(side=tk.LEFT, padx=5)

    width = popup.winfo_reqwidth()
    height = popup.winfo_reqheight()
    pos_x = int(root.winfo_screenwidth() / 2 - width / 2)
    pos_y = int(root.winfo_screenheight() / 2 - height)
    popup.geometry("+{}+{}".format(pos_x, pos_y))

    popup.mainloop()