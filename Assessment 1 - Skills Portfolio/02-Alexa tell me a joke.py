import tkinter as tk
import random
import os
import threading
import win32com.client  # Microsoft speech API


#----- USING WINDOWS VOICE CONVERT TEXT TO SPEECH -----
#  This allows the app to speak the joke aloud.
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    # By the use of threading run speaking independently
    threading.Thread(target=lambda: speaker.Speak(text, 1), daemon=True).start()
    # Flag 1 means speak independently (does not block)


# ----- FROM FILE LOAD JOKES -----
#  Each line in randomJokes.txt is expected to have:
#       setup ? punchline
#  This function extracts and stores them as tuples.

def load_jokes(filename):
    jokes = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip() 
                
                 # If it contains a question mark, assume it's a valid joke format
                if "?" in line:
                    setup, punchline = line.split("?", 1)  # Split only at first '?'
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        # Fallback joke in case the file is missing
        jokes.append(("Joke file not found!", "Please check randomJokes.txt"))
    return jokes


# Control file path
base_path = os.path.dirname(os.path.abspath(__file__))   # Folder of this script
file_path = os.path.join(base_path, "randomJokes.txt")   # Path to jokes file
jokes = load_jokes(file_path)                            # Load jokes list


# ----- FUNCTIONS OF GUI BUTTONS -----

def show_random_joke():
    """
    Select a random joke from the list and display only the setup.
    Punchline is hidden until user presses 'Show Punchline'.
    Also triggers text-to-speech for the setup line.
    """
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    show_button.config(state=tk.NORMAL)

    speak(current_joke[0])  # Speak setup


def show_punchline():
    punchline_label.config(text=current_joke[1])
    show_button.config(state=tk.DISABLED)

    speak(current_joke[1])  # Speak punchline


def quit_app():
#Close the entire application window.
    root.destroy()


# ----- GUI SETUP -----

root = tk.Tk()
root.title("Alexa - Tell me a Joke")
root.geometry("500x320")
root.config(bg="#1E1E1E")     # Dark background

# Title label at the top
title_label = tk.Label(root, text="Alexa Joke Assistant",
                       font=("Arial", 18, "bold"), fg="white", bg="#1E1E1E")
title_label.pack(pady=10)

# Label for joke setup / question
setup_label = tk.Label(root, text="", font=("Arial", 14),
                       wraplength=460, fg="#FFD700", bg="#1E1E1E",
                       justify="center")
setup_label.pack(pady=20)

# Label for punchline (initially empty) 
punchline_label = tk.Label(root, text="", font=("Arial", 14),
                           wraplength=460, fg="#90EE90", bg="#1E1E1E",
                           justify="center")
punchline_label.pack(pady=10)

# Frame to hold all buttons in a row
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=20)

# Main button - fetch a new joke
alexa_button = tk.Button(button_frame, text="Alexa tell me a Joke",
                         font=("Arial", 12, "bold"),
                         command=show_random_joke,
                         bg="#1DB954", fg="white", width=18)
alexa_button.grid(row=0, column=0, padx=5)

# Button to reveal punchline (disabled until joke shown)
show_button = tk.Button(button_frame, text="Show Punchline",
                        font=("Arial", 12, "bold"),
                        command=show_punchline,
                        bg="#FFA500", fg="black", width=15,
                        state=tk.DISABLED)
show_button.grid(row=0, column=1, padx=5)

# Button to load next joke immediately
next_button = tk.Button(button_frame, text="Next Joke",
                        font=("Arial", 12, "bold"),
                        command=show_random_joke,
                        bg="#4682B4", fg="white", width=12)
next_button.grid(row=0, column=2, padx=5)

# Quit button at bottom
quit_button = tk.Button(root, text="Quit",
                        font=("Arial", 12, "bold"),
                        command=quit_app,
                        bg="#FF4C4C", fg="white", width=10)
quit_button.pack(pady=10) 
    
# Load a joke immediately when app starts    
show_random_joke()

# Keep window running
root.mainloop()
