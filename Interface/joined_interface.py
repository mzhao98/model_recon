import tkinter as tk
import tkinter.font as TkFont
from tkVideoPlayer import TkinterVideo
import datetime
from tkinter import filedialog

# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = TkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["PageOne"] = PageOne(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["PageOne"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


# Watch video of robot attempting task
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Watch Robohelper Cut Play-Doh", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="I have a question",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()

        self.load_btn = tk.Button(self, text="Load", command=self.load_video)
        self.load_btn.pack()

        self.vid_player = TkinterVideo(scaled=True, master=self)
        self.vid_player.pack(expand=True, fill="both")

        self.play_pause_btn = tk.Button(self, text="Play", command=self.play_pause)
        self.play_pause_btn.pack()

        self.vid_player.bind("<<Ended>>", self.video_ended)

    def initiate_question(self):
        self.vid_player.pause()
        self.play_pause_btn["text"] = "Play"

        self.controller.show_frame("PageOne")

    def load_video(self):
        """ loads the video """
        file_path = filedialog.askopenfilename(filetypes=[("Mp4", "*.mp4")])

        if file_path:
            self.vid_player.load(file_path)
            self.play_pause_btn["text"] = "Play"

    def play_pause(self):
        """ pauses and plays """
        if self.vid_player.is_paused():
            self.vid_player.play()
            self.play_pause_btn["text"] = "Pause"

        else:
            self.vid_player.pause()
            self.play_pause_btn["text"] = "Play"


    def video_ended(self, event):
        """ handle video ended """
        self.play_pause_btn["text"] = "Play"

# Chat with robot
class PageOne(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Chat with RoboHelper", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="My question is resolved.",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()