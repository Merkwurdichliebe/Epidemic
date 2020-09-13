import tkinter as tk
from tkinter import ttk
from webbrowser import open as webopen


def display_help(root):
    def cb_open_web():
        webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title('Epidemic Help')
    text = 'Help is available on the application\'s GitHub page.'
    lbl1 = tk.Label(dialog, text=text, pady=10, padx=20)
    lbl1.pack()

    frm_btns = tk.Frame(dialog, pady=10)
    frm_btns.pack()

    btn = tk.Button(frm_btns, text='View in browser', width=15, command=cb_open_web)
    btn.pack(side=tk.LEFT, padx=5)
    btn = tk.Button(frm_btns, text='Close', width=15, command=dialog.destroy)
    btn.pack(side=tk.LEFT, padx=5)

    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()
    pos_x = int(root.winfo_screenwidth() / 2 - width / 2)
    pos_y = int(root.winfo_screenheight() / 2 - height)
    dialog.geometry("+{}+{}".format(pos_x, pos_y))

    dialog.grab_set()
    dialog.attributes("-topmost", True)


def display_select_game(root):
    def cb_start_game():
        dialog.destroy()
        return root.game_choice.get()

    root.game_options = ['Pandemic (regular)', 'Legacy Season 1', 'Legacy Season 2']
    root.game_choice = tk.StringVar()
    root.game_choice.set(root.game_options[0])

    dialog = tk.Toplevel()
    dialog.title('Select Game')
    text = 'Select the game you wish to track:'
    lbl1 = tk.Label(dialog, text=text, pady=10, padx=20)
    lbl1.pack()

    # TODO Why do we need to unpack the option list here and not in epidemic_options
    root.dropdown_game = tk.OptionMenu(dialog, root.game_choice, *root.game_options)
    root.dropdown_game.config(width=20)
    root.dropdown_game.pack()

    frm_btns = tk.Frame(dialog, pady=10)
    frm_btns.pack()

    btn = tk.Button(frm_btns, text='Cancel', width=15, command=dialog.destroy)
    btn.pack(side=tk.LEFT, padx=5)
    btn = tk.Button(frm_btns, text='Start New Game', width=15, command=cb_start_game)
    btn.pack(side=tk.LEFT, padx=5)

    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()
    pos_x = int(root.winfo_screenwidth() / 2 - width / 2)
    pos_y = int(root.winfo_screenheight() / 2 - height)
    dialog.geometry("+{}+{}".format(pos_x, pos_y))

    dialog.grab_set()
    dialog.attributes("-topmost", True)


class DialogHelp:
    def __init__(self, app):
        self.top = tk.Toplevel(app.view.root)
        
        text = 'Help is available on the application\'s GitHub page.'
        tk.Label(self.top, text=text, pady=10, padx=20).pack()

        frm_btns = tk.Frame(self.top, pady=10)
        frm_btns.pack()
        btn = tk.Button(frm_btns, text='View in browser', width=15, command=self.open_web)
        btn.pack(side=tk.LEFT, padx=5)
        btn = tk.Button(frm_btns, text='Close', width=15, command=self.close)
        btn.pack(side=tk.LEFT, padx=5)

    def open_web(self):
        webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')
        self.top.destroy()

    def close(self):
        self.top.destroy()


