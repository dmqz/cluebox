import gpiozero
import pygame
import time
<<<<<<< HEAD
import json
import os
import sys
=======
import tkinter as tk
import json
import os
import sys
from PIL import Image, ImageTk  # Import for image handling
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631

# Set up the GPIO pin for the button
button = gpiozero.Button(17, pull_up=True, bounce_time=0.1)

<<<<<<< HEAD
# Initialize pygame for image handling and sound playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.init()

# Set up the Pygame screen (full-screen mode)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Clue Box")

# Load background image using pygame
def load_background_image(image_path="bg.jpg"):
    try:
        bg_image = pygame.image.load(image_path)
        # Resize the image to fit the screen size
        bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))
=======
# Initialize pygame mixer for sound playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

# Create a tkinter window for displaying text
root = tk.Tk()
root.title("Clue Box")

# Make the window full screen
root.update_idletasks()
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Load the background image
def load_background_image():
    try:
        bg_image = Image.open("bg.jpg")  # Load the image
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)  # Resize to fit the screen
        bg_image = ImageTk.PhotoImage(bg_image)  # Convert to Tkinter format
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
        return bg_image
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

<<<<<<< HEAD
# Load the background image
bg_image = load_background_image()

=======
# Set the background image as the window's background
bg_image = load_background_image()

# Set up a label to display the background image
if bg_image:
    background_label = tk.Label(root, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set up a label to display text on the screen
label = tk.Label(root, text="", font=("Helvetica", 48), fg="white", bg="black", justify="center", wraplength=root.winfo_screenwidth()-50)
label.pack(expand=True)

>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
# Function to load clues from a configuration file (JSON)
def load_clues(config_file='config.json'):
    if not os.path.exists(config_file):
        print(f"Config file '{config_file}' not found.")
        return []
<<<<<<< HEAD
    
=======

>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
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
<<<<<<< HEAD
press_count = 0  # Keeps track of which clue to display
button_press_start_time = None
button_hold_duration = 3  # seconds for reset
reset_triggered = False
=======
button_press_start_time = None
button_hold_duration = 3  # seconds for reset
reset_triggered = False
press_count = 0  # Keeps track of which clue to display

# Function to adjust font size dynamically
def adjust_font_size(event=None):
    font_size = int(min(root.winfo_width(), root.winfo_height()) / 10)
    label.config(font=("Helvetica", font_size), wraplength=root.winfo_width()-50)
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631

# Function to reset the app
def reset_app():
    global reset_triggered, press_count
    if not reset_triggered:
        print("Resetting the app...")
<<<<<<< HEAD
        press_count = 0
        reset_triggered = True
        screen.fill((0, 0, 0))  # Clear the screen (black)
        pygame.display.update()
        draw_text("Welcome to the Clue Box!\nPress the button to start.", size=48)
        pygame.display.update()

# Function to draw wrapped text on screen
def draw_text(text, size=48, color=(255, 255, 255)):
    font = pygame.font.SysFont("Helvetica", size)
    words = text.split(' ')
    lines = []
    line = ""
    
    # Split text into lines based on screen width
    for word in words:
        test_line = line + " " + word if line else word
        text_width, text_height = font.size(test_line)
        if text_width <= screen.get_width() - 50:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)  # Add the last line

    y_offset = screen.get_height() // 4  # Start text in the middle of the screen

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_height  # Move down for next line
=======
        label.config(text="")
        pygame.mixer.stop()
        press_count = 0
        reset_triggered = True

# Function to smoothly transition between clues
def transition_to_clue(clue):
    label.config(text="")
    label.after(500, play_new_clue, clue)
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631

# Function to play a new clue
def play_new_clue(clue):
    pygame.mixer.stop()
    try:
        sound = pygame.mixer.Sound(clue["sound"])
        sound.play()
    except pygame.error as e:
        print(f"Error loading sound {clue['sound']}: {e}")

<<<<<<< HEAD
=======
    label.config(text=clue["text"])

>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
# Button press handler
def on_button_pressed():
    global button_press_start_time, reset_triggered, press_count
    button_press_start_time = time.time()
    print("Button Pressed!")
<<<<<<< HEAD
    
    if press_count >= len(clues):  # If all clues were played, show "No more clues"
        draw_text("No more clues.")
        pygame.display.update()
=======

    if press_count >= len(clues):  # If all clues were played, show "No more clues"
        label.config(text="No more clues.")
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
        press_count = 0  # Reset to the first clue on the next button press
    else:  # Play the next clue
        transition_to_clue(clues[press_count])
        press_count += 1

    reset_triggered = False

<<<<<<< HEAD
# Function to smoothly transition between clues
def transition_to_clue(clue):
    screen.fill((0, 0, 0))  # Fill the screen with black before displaying text
    pygame.display.update()
    draw_text(clue["text"])
    pygame.display.update()
    play_new_clue(clue)

=======
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
# Check if the button is held
def check_button_hold():
    global button_press_start_time, reset_triggered
    if button.is_pressed:
        if button_press_start_time and (time.time() - button_press_start_time) >= button_hold_duration:
            reset_app()
    else:
        button_press_start_time = None

<<<<<<< HEAD
    pygame.time.wait(100)  # Delay to avoid overwhelming the CPU

# Function to safely exit when Escape key is pressed
def exit_program():
    print("Exiting Clue Box...")
    pygame.mixer.quit()
    pygame.quit()
    sys.exit(0)

# Main loop for the Pygame window
def main():
    global press_count
    if bg_image:
        screen.blit(bg_image, (0, 0))  # Draw the background image
    pygame.display.update()

    # Start the main event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit_program()
        
        # Check if the button is pressed
        if button.is_pressed:
            on_button_pressed()

        # Check if the button is held
        check_button_hold()

    pygame.quit()

if __name__ == "__main__":
    main()
=======
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
>>>>>>> 85cb27b1797f0794a0b16c2fc16920ddced88631
