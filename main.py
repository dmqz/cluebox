import gpiozero
import pygame
import time
import tkinter as tk
import json
import os

# Set up the GPIO pin for the button
button = gpiozero.Button(17, pull_up=True, bounce_time=0.1)

# Initialize pygame mixer for sound playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

# Create a tkinter window for displaying text
root = tk.Tk()
root.title("Clue Box")

# Make the window full screen
root.update_idletasks()  # Force an update
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Set up a label to display text on the screen
label = tk.Label(root, text="", font=("Helvetica", 48), fg="white", bg="black", justify="center", wraplength=root.winfo_screenwidth()-50)
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

# Variable to track button press time and reset state
button_press_start_time = None
button_hold_duration = 3  # seconds for reset
reset_triggered = False  # Variable to ensure reset happens only once
press_count = 0  # Variable to track the press count (1 for first press, 2 for second press)

# Function to dynamically adjust the font size based on window size
def adjust_font_size(event=None):
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calculate the font size based on window dimensions (adjust this value as needed)
    font_size = int(min(window_width, window_height) / 10)

    # Update the font size of the label
    label.config(font=("Helvetica", font_size), wraplength=window_width-50)

# Function to handle the reset action
def reset_app():
    global reset_triggered, press_count
    if not reset_triggered:
        print("Resetting the app...")  # Optional: print reset in the terminal
        label.config(text="")  # Clear text on screen
        pygame.mixer.stop()  # Stop any sounds if still playing
        press_count = 0  # Reset the press count to start from the first clue
        reset_triggered = True  # Mark reset as triggered

# Function to smoothly transition between clues
def transition_to_clue(clue):
    """Handle the transition between clues smoothly"""
    # Fade out the current text
    label.config(text="")
    label.after(500, play_new_clue, clue)  # Delay before showing new clue

# Function to play a new clue
def play_new_clue(clue):
    """Play the sound and display the new clue text"""
    pygame.mixer.stop()  # Stop the current sound if still playing
    
    # Play the sound associated with the current clue
    try:
        sound = pygame.mixer.Sound(clue["sound"])
        sound.play()
    except pygame.error as e:
        print(f"Error loading sound {clue['sound']}: {e}")
    
    # Display the associated text on the screen
    label.config(text=clue["text"])

# Define the button press action
def on_button_pressed():
    global button_press_start_time, reset_triggered, press_count
    
    # Record the time when the button is pressed
    button_press_start_time = time.time()

    # Print "Button Pressed!" in the terminal
    print("Button Pressed!")
    
    # Check if there's a valid clue for the current press count
    if press_count < len(clues):
        clue = clues[press_count]
        
        # Transition smoothly to the new clue
        transition_to_clue(clue)
    else:
        print("No more clues available.")
        label.config(text="No more clues.")
    
    # Increase the press count (to go to the next clue)
    press_count += 1
    reset_triggered = False  # Reset triggered flag to allow holding reset action again

# Define the button hold check
def check_button_hold():
    global button_press_start_time, reset_triggered

    # Check if the button is being held down
    if button.is_pressed:
        # Check if the button has been held for the required duration
        if button_press_start_time and (time.time() - button_press_start_time) >= button_hold_duration:
            # If the button is held for 3 seconds, reset the app
            reset_app()
    else:
        # Reset the start time if the button is released before 3 seconds
        button_press_start_time = None

    # Continue checking
    root.after(100, check_button_hold)  # Recheck every 100ms

# Attach the button press event to the handler
button.when_pressed = on_button_pressed

# Start the continuous button hold check
root.after(100, check_button_hold)  # Check hold status every 100ms

# Bind the resize event to adjust the font size dynamically
root.bind('<Configure>', adjust_font_size)

# Run the Tkinter event loop
root.mainloop()
