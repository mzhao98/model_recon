import tkinter as tk
import tkinter.font as TkFont
from tkVideoPlayer import TkinterVideo
import datetime
from tkinter import filedialog

from Interface.Outdated.test_gpt import obtain_initial_plan, obtain_model_explanation

### Code adapted from the following
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# https://www.w3resource.com/python-exercises/tkinter/python-tkinter-layout-management-exercise-7.php 

class model_recon(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = TkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["WatchVideo"] = WatchVideo(parent=container, controller=self)
        self.frames["ChatPage"] = ChatPage(parent=container, controller=self)

        self.frames["WatchVideo"].grid(row=0, column=0, sticky="nsew")
        self.frames["ChatPage"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("WatchVideo")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

# Watch video of robot attempting task
class WatchVideo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Watch Robohelper Cut Play-Doh", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="I have a question",
                            command=lambda: controller.show_frame("ChatPage"))
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

        self.controller.show_frame("ChatPage")

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
class ChatPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Chat with RoboHelper", font=controller.title_font)
        label.grid(row=1, column=0, padx=10, pady=10)
        
        # label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="My question is resolved.",
                           command=lambda: controller.show_frame("WatchVideo"))
        # button.pack()
        button.grid(row=4, column=0, padx=10, pady=10)

        # Create a Text widget for message history
        self.message_history = tk.Text(self, wrap=tk.WORD, width=40, height=10)
        self.message_history.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.message_history.config(state=tk.DISABLED)

        # Initial robot play 
        self.message_history.config(state=tk.NORMAL)
        self.models_response = obtain_initial_plan() # "Model's initial plan"
        self.message_history.insert(tk.END, f"\nRoboHelper: {self.models_response}\n")
        self.message_history.config(state=tk.DISABLED)

        # Create an Entry widget for entering messages
        self.message_entry = tk.Entry(self, width=30)
        self.message_entry.grid(row=3, column=0, padx=10, pady=10)

        # Create a "Send" button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=3, column=1, padx=10, pady=10)


    # Function to send a message
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_history.config(state=tk.NORMAL)
            self.message_history.insert(tk.END, f"\nYou: {message}\n")
            self.message_history.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            self.message_history.config(state=tk.NORMAL)
            models_response = obtain_model_explanation(message) # "Model's explanation"
            self.message_history.insert(tk.END, f"\nRoboHelper: {models_response}\n")
            self.message_history.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = model_recon()
    app.mainloop()