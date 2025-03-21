import gpiozero
import pygame
import time
import tkinter as tk
import json
import os
import sys

# Set up the GPIO pin for the button
button = gpiozero.Button(17, pull_up=True, bounce_time=0.1)

# Initialize pygame mixer for sound playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

# Create a tkinter window for displaying text
root = tk.Tk()
root.title("Clue Box")

# Make the window full screen
root.update_idletasks()
root.attributes('-fullscreen', True)
root.configure(bg='black')
root.config(cursor="none")

# Set up a label to display text on the screen
label = tk.Label(root, text="Need a clue?", font=("Helvetica", 48), fg="white", bg="black", 
                 justify="center", wraplength=root.winfo_screenwidth()-50)
label.pack(expand=True)

# Function to load clues from a configuration file (JSON)
def load_clues(config_file='config.json'):
    if not os.path.exists(config_file):
        print(f"Config file '{config_file}' not found.")
        return []
    
    with open(config_file, 'r') as file:
        try:
            clues = json.load(file)
            return clues
        except json.JSONDecodeError:
            print(f"Error reading the config file '{config_file}'. Make sure it is valid JSON.")
            return []

# Load the clues from the config file
clues = load_clues()

# Variables
button_press_start_time = None
button_hold_duration = 3  # seconds for reset
reset_triggered = False
press_count = 0  # Keeps track of which clue to display

# Function to adjust font size dynamically
def adjust_font_size(event=None):
    font_size = int(min(root.winfo_width(), root.winfo_height()) / 10)
    label.config(font=("Helvetica", font_size), wraplength=root.winfo_width()-50)

# Function to reset the app
def reset_app():
    global reset_triggered, press_count
    if not reset_triggered:
        print("Resetting the app...")
        label.config(text="")
        pygame.mixer.stop()
        press_count = 0
        reset_triggered = True

# Function to smoothly transition between clues
def transition_to_clue(clue):
    label.config(text="")
    label.after(500, play_new_clue, clue)

# Function to play a new clue
def play_new_clue(clue):
    pygame.mixer.stop()
    try:
        sound = pygame.mixer.Sound(clue["sound"])
        sound.play()
    except pygame.error as e:
        print(f"Error loading sound {clue['sound']}: {e}")
    
    label.config(text=clue["text"])

# Button press handler
def on_button_pressed():
    global button_press_start_time, reset_triggered, press_count
    button_press_start_time = time.time()
    print("Button Pressed!")
    
    if press_count >= len(clues):  # If all clues were played, show "No more clues"
        label.config(text="No more clues. Press the green button to hear them again.")
        press_count = 0  # Reset to the first clue on the next button press
    else:  # Play the next clue
        transition_to_clue(clues[press_count])
        press_count += 1

    reset_triggered = False

# Check if the button is held
def check_button_hold():
    global button_press_start_time, reset_triggered
    if button.is_pressed:
        if button_press_start_time and (time.time() - button_press_start_time) >= button_hold_duration:
            reset_app()
    else:
        button_press_start_time = None

    root.after(100, check_button_hold)

# Function to safely exit when Escape key is pressed
def exit_program(event=None):
    print("Exiting Clue Box...")
    pygame.mixer.quit()
    root.destroy()
    sys.exit(0)

# Attach the button event
button.when_pressed = on_button_pressed

# Start checking button hold
root.after(100, check_button_hold)

# Adjust font size on window resize
root.bind('<Configure>', adjust_font_size)

# Bind the Escape key to quit the application
root.bind("<Escape>", exit_program)

# Run the Tkinter event loop
root.mainloop()
