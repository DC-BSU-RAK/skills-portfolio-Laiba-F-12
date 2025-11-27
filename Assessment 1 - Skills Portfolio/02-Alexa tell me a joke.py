import tkinter as tk
import random
import os
import pyttsx3
import threading
import queue

# ----- SETUP TEXT-TO-SPEECH -----
engine = pyttsx3.init()

# Optional: set female voice like Alexa
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

speech_queue = queue.Queue()

def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:  # sentinel to stop thread if needed
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Start speech thread
threading.Thread(target=speech_worker, daemon=True).start()

# Simple speak function
def speak(text):
    speech_queue.put(text)


# ----- FROM FILE LOAD JOKES -----
def load_jokes(filename):
    jokes = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip() 
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        jokes.append(("Joke file not found!", "Please check randomJokes.txt"))
    return jokes


# Control file path
base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "randomJokes.txt")
jokes = load_jokes(file_path)


# ----- FUNCTIONS OF GUI BUTTONS -----
def show_random_joke():
    global current_joke
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")
    show_button.config(state=tk.NORMAL)
    
    speak(current_joke[0])  # speaks reliably

def show_punchline():
    punchline_label.config(text=current_joke[1])
    show_button.config(state=tk.DISABLED)
    
    speak(current_joke[1])  # speaks reliably

def quit_app():
    root.destroy()


# ----- GUI SETUP -----
root = tk.Tk()
root.title("Alexa - Tell me a Joke")
root.geometry("500x320")
root.config(bg="#1E1E1E")

title_label = tk.Label(root, text="Alexa Joke Assistant",
                       font=("Arial", 18, "bold"), fg="white", bg="#1E1E1E")
title_label.pack(pady=10)

setup_label = tk.Label(root, text="", font=("Arial", 14),
                       wraplength=460, fg="#FFD700", bg="#1E1E1E",
                       justify="center")
setup_label.pack(pady=20)

punchline_label = tk.Label(root, text="", font=("Arial", 14),
                           wraplength=460, fg="#90EE90", bg="#1E1E1E",
                           justify="center")
punchline_label.pack(pady=10)

button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=20)

alexa_button = tk.Button(button_frame, text="Alexa tell me a Joke",
                         font=("Arial", 12, "bold"),
                         command=show_random_joke,
                         bg="#1DB954", fg="white", width=18)
alexa_button.grid(row=0, column=0, padx=5)

show_button = tk.Button(button_frame, text="Show Punchline",
                        font=("Arial", 12, "bold"),
                        command=show_punchline,
                        bg="#FFA500", fg="black", width=15,
                        state=tk.DISABLED)
show_button.grid(row=0, column=1, padx=5)

next_button = tk.Button(button_frame, text="Next Joke",
                        font=("Arial", 12, "bold"),
                        command=show_random_joke,
                        bg="#4682B4", fg="white", width=12)
next_button.grid(row=0, column=2, padx=5)

quit_button = tk.Button(root, text="Quit",
                        font=("Arial", 12, "bold"),
                        command=quit_app,
                        bg="#FF4C4C", fg="white", width=10)
quit_button.pack(pady=10) 
    
    
# Load a joke immediately when app starts    
show_random_joke()

# Keep window running
root.mainloop()
