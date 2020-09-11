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


def display_select_game(root):
    def cb_start_game():
        popup.destroy()
        return root.game_choice

    root.game_options = ['Pandemic (regular)', 'Legacy Season 1', 'Legacy Season 2']
    root.game_choice = tk.StringVar()
    root.game_choice.set(root.game_options[0])

    popup = tk.Toplevel()
    popup.title('Select Game')
    text = 'Select the game you wish to track:'
    lbl1 = tk.Label(popup, text=text, pady=10, padx=20)
    lbl1.pack()

    # TODO Why do we need to unpack the option list here and not in epidemic_options
    root.dropdown_game = tk.OptionMenu(popup, root.game_choice, *root.game_options)
    root.dropdown_game.config(width=20)
    root.dropdown_game.pack()

    frm_btns = tk.Frame(popup, pady=10)
    frm_btns.pack()

    btn = tk.Button(frm_btns, text='Cancel', width=15, command=popup.destroy)
    btn.pack(side=tk.LEFT, padx=5)
    btn = tk.Button(frm_btns, text='Start New Game', width=15, command=cb_start_game)
    btn.pack(side=tk.LEFT, padx=5)