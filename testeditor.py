import tkinter as tk
import os
import sys

def create_cube(event):
    if not is_dragging.get():
        x, y = event.x, event.y
        cube = canvas.create_rectangle(x-15, y-15, x+15, y+15, fill="red", outline="", tags="cube")
        cubes.append(cube)

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
    x1, y1, x2, y2 = canvas.bbox(selected_cube) # type: ignore
    mid_y = (y1 + y2) / 2
    snap_y = None
    min_dist = float('inf')
    for cube in cubes:
        if cube != selected_cube:
            cx1, cy1, cx2, cy2 = canvas.bbox(cube)
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
    if is_dragging.get():
        x, y = event.x, event.y
        if selected_cube:
            dx, dy = x - prev_x, y - prev_y
            canvas.move(selected_cube, dx, dy)
            prev_x, prev_y = x, y
            snap_to_cube()

def drag_stop(event):
    is_dragging.set(False)

def delete_cube(event):
    canvas.delete(tk.CURRENT)

def leave_game():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"python {script_dir}/player.py")
    root.destroy()
    sys.exit()

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

is_dragging = tk.BooleanVar()
is_dragging.set(False)
selected_cube = None
prev_x, prev_y = 0, 0
cubes = []

block_button.bind("<Button-1>", lambda event: canvas.bind("<Button-1>", create_cube))
canvas.tag_bind("cube", "<ButtonPress-1>", drag_start)
canvas.bind("<B1-Motion>", drag_motion)
canvas.bind("<ButtonRelease-1>", drag_stop)
canvas.bind("<Button-3>", delete_cube)

root.mainloop()
