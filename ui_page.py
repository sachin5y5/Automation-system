import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os

def run_ui(ui_running):
    # Ensure the GIF path is correct
    gif_path = "C:/Users/Sachin/OneDrive/Desktop/rasa/Untitled design.gif"
    if not os.path.exists(gif_path):
        print(f"Error: GIF not found at {gif_path}")
        return  # Exit if the GIF is not found

    # Create the main window
    root = tk.Tk()
    root.title("Speech Recognition UI")
    root.configure(bg="black")

    # Maximize the window without hiding the taskbar
    root.state('zoomed')
    root.update_idletasks()  # Ensure the window dimensions are accurate

    try:
        gif = Image.open(gif_path)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight() - 40  # Adjust height to account for the taskbar
        frames = [ImageTk.PhotoImage(frame.copy().resize((screen_width, screen_height), Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(gif)]
        frame_count = len(frames)

        label = tk.Label(root, bg="black")
        label.place(x=0, y=0, relwidth=1, relheight=1)

        def update_frame(index):
            if not ui_running[0]:
                return  # Stop updating frames if the UI is closed
            frame = frames[index]
            label.config(image=frame)
            root.after(100, update_frame, (index + 1) % frame_count)  # Update frame every 100ms

        update_frame(0)  # Start the animation
    except Exception as e:
        label = tk.Label(root, text=f"Error loading GIF: {e}", bg="black", fg="white", font=("Arial", 20))
        label.pack(expand=True)

    # Add a key binding to exit the window (e.g., pressing 'Esc')
    root.bind("<Escape>", lambda e: exit_ui(root, ui_running))

    # Periodically check if the UI should close
    def check_ui_running():
        if not ui_running[0]:
            root.quit()  # Exit the Tkinter main loop
        else:
            root.after(100, check_ui_running)

    root.after(100, check_ui_running)
    root.mainloop()

def exit_ui(root, ui_running):
    ui_running[0] = False  # Signal the backend thread to stop
    root.quit()  # Exit the Tkinter main loop
    root.destroy()  # Close the UI
