import tkinter as tk
import os

def login():
    username = username_entry.get()
    password = password_entry.get()

    accounts = [
        {"username": "shadow", "password": "2023"},
        {"username": "glitch", "password": "0000"},
        {"username": "guest", "password": "guest"}
    ]

    account = next((acc for acc in accounts if acc["username"] == username and acc["password"] == password), None)
    if account:
        login_frame.pack_forget()
        window.title("Ripple")
        logged_in_label.config(text=account['username'], font=("Arial", 14, "bold"))  # Adjust font size here
        logged_in_label.pack(side=tk.TOP, anchor=tk.E)
        logout_button.pack(side=tk.TOP)
        first_game_button.pack(side=tk.TOP)
        open_editor_button.pack(side=tk.TOP)  # Added button for opening editor
    else:
        error_label.config(text="Invalid username or password.")

def logout():
    login_frame.pack()
    logged_in_label.pack_forget()
    logout_button.pack_forget()
    first_game_button.pack_forget()
    open_editor_button.pack_forget()  # Hide open editor button on logout
    error_label.config(text="")
    window.title("Ripple")
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def show_coming_soon():
    coming_soon_label.pack()
    login_button.pack_forget()
    first_game_button.pack_forget()
    open_editor_button.pack_forget()  # Hide open editor button on 'The first game' click
    logout_button.pack_forget()
    error_label.pack_forget()
    window.after(3000, hide_coming_soon)

def hide_coming_soon():
    coming_soon_label.pack_forget()
    login_button.pack()
    first_game_button.pack()
    open_editor_button.pack()  # Show open editor button after 'Coming Soon' disappears
    logout_button.pack()
    error_label.pack()

def open_editor():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    editor_path = os.path.join(script_dir, 'testeditor.py')
    os.system(f'python {editor_path}')  # Replace 'python' with your Python interpreter if needed

window = tk.Tk()
window.title("Ripple")
window.configure(bg="#000")
window.state('zoomed')  # Maximize the window

login_frame = tk.Frame(window, bg="#000")
login_frame.pack()

tk.Label(login_frame, text="Ripple", font=("Arial", 18), fg="#fff", bg="#000").pack()

username_entry = tk.Entry(login_frame)
username_entry.pack()

password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack()

error_label = tk.Label(login_frame, fg="red", bg="#000")
error_label.pack()

logged_in_label = tk.Label(window, fg="#fff", bg="#000")
logout_button = tk.Button(window, text="Logout", command=logout, bg="#000", fg="#fff")
first_game_button = tk.Button(window, text="The first game", bg="#000", fg="#fff", command=show_coming_soon)
open_editor_button = tk.Button(window, text="Open Editor", bg="#000", fg="#fff", command=open_editor)

coming_soon_label = tk.Label(window, text="Coming Soon", font=("Arial", 24), bg="#000", fg="#fff")

window.mainloop()
