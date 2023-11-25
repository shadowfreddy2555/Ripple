import os
import tkinter as tk
import tkinter.colorchooser as cc

def create_cube(event):
    if not is_dragging.get() and not is_playing.get():
        x, y = event.x, event.y
        cube = canvas.create_rectangle(x-15, y-15, x+15, y+15, fill=current_color, outline="", tags="cube")
        cubes.append(cube)
        save_cube_info(cube, x, y, current_color)

def save_cube_info(cube_id, x, y, color):
    cube_info = f"size=50x50,color={color},position={x}x{y}\n"
    cubes_data[cube_id] = cube_info

def drag_start(event):
    global selected_cube, prev_x, prev_y
    x, y = event.x, event.y
    items = canvas.find_overlapping(x, y, x, y)
    if items:
        selected_cube = items[-1]
        prev_x, prev_y = x, y
        is_dragging.set(True)
        canvas.tag_raise(selected_cube)

def snap_to_cube():
    global selected_cube, cubes
    if selected_cube in cubes:
        bbox = canvas.bbox(selected_cube)
        if bbox:
            x1, y1, x2, y2 = bbox
            mid_y = (y1 + y2) / 2
            snap_y = None
            min_dist = float('inf')
            for cube in cubes:
                if cube != selected_cube:
                    bbox_c = canvas.bbox(cube)
                    if bbox_c:
                        cx1, cy1, cx2, cy2 = bbox_c
                        mid_cx = (cx1 + cx2) / 2
                        mid_cy = (cy1 + cy2) / 2
                        dist_x = abs((x1 + x2) / 2 - mid_cx)
                        dist_y = abs(mid_y - mid_cy)
                        if dist_x <= 150 and dist_y <= 1 and dist_y < min_dist:
                            min_dist = dist_y
                            snap_y = mid_cy
            if snap_y is not None:
                canvas.move(selected_cube, 0, snap_y - mid_y)

def drag_motion(event):
    global prev_x, prev_y
    if is_dragging.get() and not is_playing.get():
        x, y = event.x, event.y
        if selected_cube:
            dx, dy = x - prev_x, y - prev_y
            canvas.move(selected_cube, dx, dy)
            prev_x, prev_y = x, y
            snap_to_cube()


def drag_stop(event):
    is_dragging.set(False)

def delete_cube(event):
    cube_ids = event.widget.find_withtag(tk.CURRENT)
    if cube_ids:
        cube_id = cube_ids[0]
        canvas.delete(cube_id)
        if cube_id in cubes_data:
            del cubes_data[cube_id]


def leave_game():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"python {script_dir}/player.py")
    root.destroy()
    sys.exit()

def change_color():
    global current_color
    color = cc.askcolor()[1]  # Returns the chosen color as a hex value
    if color:
        current_color = color

def select_color():
    global current_color
    color = cc.askcolor(color=current_color)[1]  # Returns the chosen color as a hex value
    if color:
        current_color = color

def toggle_background():
    global is_dark_mode
    if is_dark_mode:
        root.config(bg="white")
        canvas.config(bg="white")
        is_dark_mode = False
    else:
        root.config(bg="black")
        canvas.config(bg="black")
        is_dark_mode = True

def undo(event):
    if cubes:
        cube_id = cubes.pop()
        canvas.delete(cube_id)
        if cube_id in cubes_data:
            del cubes_data[cube_id]

def save_data():
    game_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glitch")
    values_file = os.path.join(game_folder, "values.txt")

    with open(values_file, "w") as file:
        file.write("")  # Clearing the file

    for cube_id, data in cubes_data.items():
        with open(values_file, "a") as file:
            file.write(data)

def load_data():
    game_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glitch")
    values_file = os.path.join(game_folder, "values.txt")

    with open(values_file, "r") as file:
        lines = file.readlines()

    for cube_id in cubes_data:
        canvas.delete(cube_id)
    cubes_data.clear()

    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 3:
            size = parts[0].split("=")[1]
            color = parts[1].split("=")[1]
            position = parts[2].split("=")[1]

            position_x, position_y = map(int, position.split("x"))
            cube = canvas.create_rectangle(position_x - 15, position_y - 15, position_x + 15, position_y + 15, fill=color, outline="", tags="cube")
            cubes.append(cube)
            cubes_data[cube] = f"size={size},color={color},position={position}\n"

def add_movement():
    global is_moving
    is_moving = True

def play_game():
    global is_playing, is_moving
    is_playing.set(True)
    is_moving = True
    hide_editor_buttons()

def move_selected_cube(key):
    global selected_cube, cubes, canvas
    if selected_cube in cubes:
        dx, dy = 0, 0
        if key == 'w':
            dy = -5
        elif key == 's':
            dy = 5
        elif key == 'a':
            dx = -5
        elif key == 'd':
            dx = 5
        canvas.move(selected_cube, dx, dy)
        snap_to_cube()

def stop_game():
    global is_playing, is_moving
    is_playing.set(False)
    is_moving = False
    show_editor_buttons()
    reset_movement()

def hide_editor_buttons():
    for button in editor_buttons:
        button.pack_forget()
    play_button.pack_forget()
    stop_button.pack(side=tk.LEFT)

def show_editor_buttons():
    for button in editor_buttons:
        button.pack(side=tk.LEFT)
    play_button.pack(side=tk.LEFT)
    stop_button.pack_forget()

def reset_movement():
    pass  # Reset any movement made during the game

def move_cubes(event):
    global is_moving
    if is_moving and is_playing.get():
        key = event.keysym
        if key in ('w', 'a', 's', 'd'):
            move_selected_cube(key)


def move_direction(key):
    global selected_cube, cubes
    if is_playing.get() and is_moving:
        if selected_cube in cubes:
            dx, dy = 0, 0
            if key == 'w':
                dy = -10
            elif key == 's':
                dy = 10
            elif key == 'a':
                dx = -10
            elif key == 'd':
                dx = 10
            canvas.move(selected_cube, dx, dy)
            snap_to_cube()


root = tk.Tk()
root.title("Cube Creator")
root.state('zoomed')  # Start the window maximized

canvas = tk.Canvas(root, bg="white")
canvas.pack(expand=True, fill="both")

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

block_button = tk.Button(button_frame, text="Block")
block_button.pack(side=tk.LEFT)

leave_button = tk.Button(button_frame, text="Leave Game", command=leave_game)
leave_button.pack(side=tk.LEFT)

color_button = tk.Button(button_frame, text="Change Color", command=select_color)
color_button.pack(side=tk.LEFT)

dark_button = tk.Button(button_frame, text="Dark", command=toggle_background)
dark_button.pack(side=tk.LEFT)

save_button = tk.Button(button_frame, text="Save", command=save_data)
save_button.pack(side=tk.LEFT)

load_button = tk.Button(button_frame, text="Load", command=load_data)
load_button.pack(side=tk.LEFT)

movement_button = tk.Button(button_frame, text="Add Movement to Game", command=add_movement)
movement_button.pack(side=tk.LEFT)

play_button = tk.Button(button_frame, text="Play", command=play_game)
play_button.pack(side=tk.LEFT)

stop_button = tk.Button(button_frame, text="Stop", command=stop_game)

editor_buttons = [block_button, leave_button, color_button, dark_button, save_button, load_button, movement_button]
is_dragging = tk.BooleanVar()
is_dragging.set(False)
is_playing = tk.BooleanVar()
is_playing.set(False)
selected_cube = None
prev_x, prev_y = 0, 0
cubes = []
cubes_data = {}
current_color = "red"  # Default color
is_dark_mode = False  # Flag for dark mode
is_moving = False  # Flag for cube movement

block_button.bind("<Button-1>", lambda event: canvas.bind("<Button-1>", create_cube))
canvas.tag_bind("cube", "<ButtonPress-1>", drag_start)
canvas.bind("<B1-Motion>", drag_motion)
canvas.bind("<ButtonRelease-1>", drag_stop)
canvas.bind("<Button-3>", delete_cube)
root.bind("<Control-z>", undo)  # Bind Ctrl + Z to the undo function
root.bind("<KeyPress>", move_cubes)

root.mainloop()
