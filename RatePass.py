import re
import urllib.request
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def check_password_strength(password):
    # Criteria for a strong password
    length_criteria = len(password) >= 12
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'[0-9]', password) is not None
    special_char_criteria = re.search(r'[\W_]', password) is not None

    # Check against common passwords
    common_passwords = []
    try:
        with open('common_passwords.txt', 'r') as file:
            common_passwords = file.read().splitlines()
    except FileNotFoundError:
        # Download a sample list of common passwords if the file is missing
        url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
        try:
            urllib.request.urlretrieve(url, 'common_passwords.txt')
            with open('common_passwords.txt', 'r') as file:
                common_passwords = file.read().splitlines()
        except Exception as e:
            print(f"Error downloading common passwords list: {e}")
            # Notify user
            messagebox.showwarning("Download Error", "Could not download the list of common passwords.")

    common_password_criteria = password not in common_passwords

    # Calculate score based on criteria
    score = sum([
        length_criteria,
        uppercase_criteria,
        lowercase_criteria,
        digit_criteria,
        special_char_criteria,
        common_password_criteria
    ])

    return score, length_criteria, uppercase_criteria, lowercase_criteria, digit_criteria, special_char_criteria, common_password_criteria

def show_custom_message(title, message, score=None):
    custom_window = Toplevel(app)
    custom_window.title(title)
    custom_window.geometry("300x200")
    
    style = ttk.Style()
    style.configure('Yellow.TButton', background='yellow', foreground='black', borderwidth=2, relief='solid', font=('Helvetica', 12))

    label = ttk.Label(custom_window, text=message, font=("Helvetica", 12))
    label.pack(pady=10, padx=10)

    if score is not None:
        score_label = ttk.Label(custom_window, text=f"Overall Score: {score} out of 6", font=("Helvetica", 12))
        score_label.pack(pady=5)

    ok_button = ttk.Button(custom_window, text="OK", command=custom_window.destroy, style='Yellow.TButton')
    ok_button.pack(pady=10)

def show_password_strength():
    password = password_entry.get()
    score, length, upper, lower, digit, special, common = check_password_strength(password)

    report = [
        f"Length (12+): {'✓' if length else '✗'}",
        f"Uppercase: {'✓' if upper else '✗'}",
        f"Lowercase: {'✓' if lower else '✗'}",
        f"Digit: {'✓' if digit else '✗'}",
        f"Special Character: {'✓' if special else '✗'}",
        f"Not a common password: {'✓' if common else '✗'}",
    ]

    report_text = "\n".join(report)
    message = f"{report_text}\n\nOverall Score: {score} out of 6"

    if score == 6:
        show_custom_message("Strength", "Your password is strong!\n\n" + message, score)
    elif 4 <= score < 6:
        show_custom_message("Strength", "Your password is fairly strong, but could be improved.\n\n" + message, score)
    else:
        show_custom_message("Strength", "Your password is weak, consider making it stronger.\n\n" + message, score)

# Set up the GUI
app = ttk.Window(themename="flatly")
app.title("RatePass")

# Set the window icon using both methods
try:
    icon_path = 'icon.ico'
    if os.path.isfile(icon_path):
        app.iconbitmap(icon_path)  # For Windows
    else:
        raise FileNotFoundError(f"Icon file '{icon_path}' not found.")
except Exception as e:
    print(f"Error setting icon with iconbitmap: {e}")

try:
    img = Image.open('icon.png')  # Load your PNG file if needed
    app.iconphoto(True, ImageTk.PhotoImage(img))  # Set the icon
except Exception as e:
    print(f"Error setting icon with iconphoto: {e}")

# Label
password_label = ttk.Label(app, text="Enter your password:", font=("Helvetica", 12))
password_label.pack(pady=10)

# Entry for password input
password_entry = ttk.Entry(app, width=30, show='*')
password_entry.pack(pady=5)

# Style for the button
style = ttk.Style()
style.configure('Yellow.TButton', background='yellow', foreground='black', borderwidth=2, relief='solid', font=('Helvetica', 12))

# Button to check password
check_button = ttk.Button(app, text="Check Password", command=show_password_strength, style='Yellow.TButton')
check_button.pack(pady=20)

# Run the GUI application
app.geometry("400x250")
app.mainloop()
