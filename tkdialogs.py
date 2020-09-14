import tkinter as tk
from webbrowser import open as webopen


class DialogHelp:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        self.top.attributes("-topmost", True)
        
        text = 'Help is available on the application\'s GitHub page.'
        tk.Label(self.top, text=text, pady=10, padx=20).pack()

        frm_btns = tk.Frame(self.top, pady=10)
        frm_btns.pack()

        btn = tk.Button(frm_btns, text='View in browser',
                        width=15, command=self.cb_open_web)
        btn.pack(side=tk.LEFT, padx=5)
        btn = tk.Button(frm_btns, text='Close',
                        width=15, command=self.cb_close)
        btn.pack(side=tk.LEFT, padx=5)

        width = self.top.winfo_reqwidth()
        height = self.top.winfo_reqheight()
        pos_x = int(self.top.winfo_screenwidth() / 2 - width / 2)
        pos_y = int(self.top.winfo_screenheight() / 2 - height)
        self.top.geometry("+{}+{}".format(pos_x, pos_y))

    def cb_open_web(self):
        webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')
        self.top.destroy()

    def cb_close(self):
        self.top.destroy()


class DialogNewGame:
    """Display a dialog box for selecting a game type.
    Expects the parent window and a list of game strings."""
    def __init__(self, parent, games):
        self.top = tk.Toplevel(parent)
        self.top.title('Select Game')
        self.top.transient(parent)
        self.top.focus_set()
        self.top.grab_set()

        self.game_options = games
        self.game_choice = tk.StringVar()
        self.game_choice.set(self.game_options[0])

        text = 'Select the game you wish to track:'
        tk.Label(self.top, text=text, pady=10, padx=20).pack()

        # TODO Why do we need to unpack the option list here
        #  and not in epidemic_options
        self.dropdown_game = tk.OptionMenu(self.top, self.game_choice,
                                           *self.game_options)
        self.dropdown_game.config(width=20)
        self.dropdown_game.pack()

        frm_btns = tk.Frame(self.top, pady=10)
        frm_btns.pack()

        btn = tk.Button(frm_btns, text='Cancel',
                        width=15, command=self.cb_cancel)
        btn.pack(side=tk.LEFT, padx=5)
        btn = tk.Button(frm_btns, text='Start New Game',
                        width=15, command=self.cb_start_game)
        btn.pack(side=tk.LEFT, padx=5)

        width = self.top.winfo_reqwidth()
        height = self.top.winfo_reqheight()
        pos_x = int(self.top.winfo_screenwidth() / 2 - width / 2)
        pos_y = int(self.top.winfo_screenheight() / 2 - height)
        self.top.geometry("+{}+{}".format(pos_x, pos_y))

    def cb_cancel(self):
        self.game_choice = None
        self.top.destroy()

    def cb_start_game(self):
        self.top.destroy()

