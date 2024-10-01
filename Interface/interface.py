import tkinter as tk
import tkinter.font as TkFont
from tkVideoPlayer import TkinterVideo

class ModelRecon(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = TkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WatchVideo, ChatPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WatchVideo")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class WatchVideo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Watch Robohelper Cut Play-Doh", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # "I have a question" button is initially hidden
        self.question_btn = tk.Button(self, text="I have a question", command=self.ask_question)
        self.question_btn.pack_forget()  # Hide button initially

        self.vid_player = TkinterVideo(scaled=True, master=self)
        self.vid_player.pack(expand=True, fill="both")

        self.play_pause_btn = tk.Button(self, text="Play", command=self.play_pause)
        self.play_pause_btn.pack()

        # Automatically load the video on startup
        self.load_video("Interface/video.mp4")

        self.vid_player.bind("<<Ended>>", self.video_ended)

    def load_video(self, file_path):
        """Loads the video."""
        if file_path:
            self.vid_player.load(file_path)
            self.play_pause_btn["text"] = "Play"

    def play_pause(self):
        """Pauses and plays the video. Shows the question button on first play."""
        if self.vid_player.is_paused():
            self.vid_player.play()
            self.play_pause_btn["text"] = "Pause"

            # Show the "I have a question" button when video is playing
            self.question_btn.pack()

        else:
            self.vid_player.pause()
            self.play_pause_btn["text"] = "Play"

    def ask_question(self):
        """Pauses the video, updates the Play button, and switches to the chat page."""
        self.vid_player.pause()  # Pause the video when the button is pressed
        self.play_pause_btn["text"] = "Play"  # Update the Play/Pause button text
        self.controller.show_frame("ChatPage")

    def video_ended(self, event):
        """Handle video ended event."""
        self.play_pause_btn["text"] = "Play"


class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="Chat with RoboHelper", font=controller.title_font)
        label.grid(row=1, column=0, padx=10, pady=10)

        tk.Button(self, text="My question is resolved.", command=lambda: controller.show_frame("WatchVideo")).grid(row=4, column=0, padx=10, pady=10)

        self.message_history = tk.Text(self, wrap=tk.WORD, width=40, height=10)
        self.message_history.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.message_history.config(state=tk.DISABLED)

        self.display_initial_response()

        self.message_entry = tk.Entry(self, width=30)
        self.message_entry.grid(row=3, column=0, padx=10, pady=10)

        tk.Button(self, text="Send", command=self.send_message).grid(row=3, column=1, padx=10, pady=10)

        # Bind the "Enter" key to the send_message method
        self.message_entry.bind("<Return>", self.send_message_key)

    def display_initial_response(self):
        self.message_history.config(state=tk.NORMAL)
        self.models_response = "hey hey hey"  # Replace with obtain_initial_plan() if using external function
        self.message_history.insert(tk.END, f"\nRoboHelper: {self.models_response}\n")
        self.message_history.config(state=tk.DISABLED)

    def send_message(self):
        """Method to handle message sending when "Send" button is pressed."""
        message = self.message_entry.get()
        if message:
            self.message_history.config(state=tk.NORMAL)
            self.message_history.insert(tk.END, f"\nYou: {message}\n")
            self.message_history.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            models_response = "oh hey there"  # Replace with obtain_model_explanation(message) if using external function
            self.message_history.config(state=tk.NORMAL)
            self.message_history.insert(tk.END, f"\nRoboHelper: {models_response}\n")
            self.message_history.config(state=tk.DISABLED)

    def send_message_key(self, event):
        """Method to handle message sending when the "Enter" key is pressed."""
        self.send_message()  # Call the same send_message function


if __name__ == "__main__":
    app = ModelRecon()
    app.mainloop()
