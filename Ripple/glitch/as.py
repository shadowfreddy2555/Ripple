import tkinter as tk
import os

# Global variables
cubes = []

def create_cube(size, color, position):
    global cubes, canvas
    # Extracting size values
    size_values = size.split('x')
    cube_width = int(size_values[0])
    cube_height = int(size_values[1])

    # Extracting position values
    position_values = position.split('x')
    x_position = int(position_values[0])
    y_position = int(position_values[1])

    # Create cube based on extracted values
    cube = canvas.create_rectangle(
        x_position, y_position, x_position + cube_width, y_position + cube_height,
        fill=color, outline=''
    )
    cubes.append((cube, x_position, y_position, cube_width, cube_height, color))

def move_cubes(event):
    global cubes, canvas
    key = event.keysym
    for idx, (cube, x_pos, y_pos, width, height, color) in enumerate(cubes):
        dx, dy = 0, 0
        if key == 'w':
            dy = -5
        elif key == 's':
            dy = 5
        elif key == 'a':
            dx = -5
        elif key == 'd':
            dx = 5
        canvas.move(cube, dx, dy)
        # Update the cube's position after movement
        x_pos += dx
        y_pos += dy
        cubes[idx] = (cube, x_pos, y_pos, width, height, color)

# Find the game folder and values.txt file
for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    if 'values.txt' in filenames:
        game_folder = dirpath
        break
else:
    raise FileNotFoundError("values.txt not found in any subdirectory of the current working directory.")

values_file = os.path.join(game_folder, 'values.txt')

# Create main window
root = tk.Tk()
root.title("Cube Drawer")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to screen dimensions
root.geometry(f"{screen_width}x{screen_height}")

# Create canvas
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

# Read values from the file in the game folder
with open(values_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        parameters = line.split(',')
        size = parameters[0].split('=')[1]
        color = parameters[1].split('=')[1]
        position = parameters[2].split('=')[1]

        # Create cube based on extracted values
        create_cube(size, color, position)

root.bind('<KeyPress>', move_cubes)
root.mainloop()
