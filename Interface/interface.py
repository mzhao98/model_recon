import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

# Create a video player object
videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load("video.mov")
videoplayer.pack(expand=True, fill="both")

# Add controls
videoplayer.play() # Start playing the video
videoplayer.pause() # Pause the video
videoplayer.stop() # Stop the video
videoplayer.set_volume(0.5) # Set volume (0-1)

root.mainloop()