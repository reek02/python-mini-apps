import qrcode
from PIL import Image, ImageTk
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, Label

def generate_qr():
    url = entry_url.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return

    folder_path = filedialog.askdirectory(title="Select Folder to Save QR Code")
    if not folder_path:
        messagebox.showwarning("Folder Error", "Please select a folder")
        return

    file_path = os.path.join(folder_path, "qr_code.png")

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="white", back_color="black")
    img.save(file_path)
    
    messagebox.showinfo("Success", f"QR Code saved at {file_path}")
    
    show_qr_image(file_path)

# 2nd window to display qr
def show_qr_image(file_path):
    new_window = Toplevel(window)
    new_window.title("Generated QR Code")
    new_window.geometry("450x450") 
    
    # Load and display the image
    try:
        qr_image = Image.open(file_path)
        qr_image = qr_image.resize((300, 300), Image.Resampling.LANCZOS) 
        img_tk = ImageTk.PhotoImage(qr_image)
        
        label_img = Label(new_window, image=img_tk)
        label_img.image = img_tk  # Keep a reference to avoid garbage collection
        label_img.pack(padx=20, pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load image: {str(e)}")

# Function to exit the application
def exit_app():
    window.quit()

# Set up the UI 
ctk.set_appearance_mode("dark") 
window = ctk.CTk()
window.title("QR Code Generator")
window.geometry("400x300")


label_title = ctk.CTkLabel(window, text="QR Code Generator", font=("Arial", 20, "bold"))
label_title.pack(pady=20)

label_url = ctk.CTkLabel(window, text="Enter URL:", font=("Arial", 14))
label_url.pack(pady=10)

entry_url = ctk.CTkEntry(window, width=300, font=("Arial", 12))
entry_url.pack(pady=5)

generate_button = ctk.CTkButton(window, text="Generate QR Code", command=generate_qr)
generate_button.pack(pady=20)

exit_button = ctk.CTkButton(window, text="Exit", command=exit_app)
exit_button.pack(pady=10)

window.mainloop()
